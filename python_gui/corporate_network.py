"""Logical companion model for the Corporate Office Network project.
This model does not configure Packet Tracer or transmit real packets.
"""
import re
from datetime import datetime
from threading import RLock

DEPARTMENTS = {
    "hr-pc": {"label": "HR PC", "department": "HR", "vlan": 10, "subnet": "192.168.10.0/24", "gateway": "192.168.10.1"},
    "finance-pc": {"label": "Finance PC", "department": "Finance", "vlan": 20, "subnet": "192.168.20.0/24", "gateway": "192.168.20.1"},
    "it-pc": {"label": "IT PC", "department": "IT", "vlan": 30, "subnet": "192.168.30.0/24", "gateway": "192.168.30.1"},
    "sales-pc": {"label": "Sales PC", "department": "Sales", "vlan": 40, "subnet": "192.168.40.0/24", "gateway": "192.168.40.1"},
}
SERVERS = {
    "dns-server": {"label": "DNS Server", "ip": "192.168.50.10", "services": ["DNS UDP/TCP 53"]},
    "dhcp-server": {"label": "DHCP Server", "ip": "192.168.50.11", "services": ["DHCP UDP 67/68"]},
    "web-server": {"label": "Intranet Web Server", "ip": "192.168.50.20", "services": ["HTTP TCP 80"]},
    "email-server": {"label": "Email Server", "ip": "192.168.50.30", "services": ["SMTP", "POP3"]},
}
DNS_RECORDS = {
    "intranet.corp.local": "192.168.50.20",
    "mail.corp.local": "192.168.50.30",
    "dns.corp.local": "192.168.50.10",
    "dhcp.corp.local": "192.168.50.11",
}

MAX_PCS_PER_DEPARTMENT = 12
MAX_ADD_AT_ONCE = 10
FIRST_HOST = 100
NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 _.\-]{0,23}$")


def _slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def _fail(reason):
    return {"success": False, "reason": reason}


class CorporateNetwork:
    def __init__(self):
        self._lock = RLock()
        self.pcs = {}
        self._load_default_pcs()
        self.reset()

    def _load_default_pcs(self):
        self.pcs = {}
        for key, d in DEPARTMENTS.items():
            self.pcs[key] = {"id": key, "label": d["label"], "department": d["department"], "vlan": d["vlan"],
                             "subnet": d["subnet"], "gateway": d["gateway"], "host": FIRST_HOST, "default": True}

    def _resolve_department(self, value):
        v = str(value or "").strip().lower()
        for key, d in DEPARTMENTS.items():
            if v in (key.lower(), d["department"].lower(), str(d["vlan"])):
                return d
        return None

    def _pc_view(self, pc):
        out = dict(pc)
        out["ip"] = f"192.168.{pc['vlan']}.{pc['host']}"
        out["has_lease"] = pc["id"] in self.leases
        return out

    def add_pcs(self, department, name=None, count=1):
        with self._lock:
            dept = self._resolve_department(department)
            if not dept:
                return _fail("Unknown department")
            try:
                count = int(count)
            except (TypeError, ValueError):
                return _fail("Number of PCs must be a whole number")
            if not 1 <= count <= MAX_ADD_AT_ONCE:
                return _fail(f"You can add between 1 and {MAX_ADD_AT_ONCE} PCs at a time")
            name = (name or "").strip()
            if name and not NAME_RE.match(name):
                return _fail("Names must be 1-24 characters: letters, numbers, spaces, - _ .")
            dname = dept["department"]
            current = [p for p in self.pcs.values() if p["department"] == dname]
            if len(current) + count > MAX_PCS_PER_DEPARTMENT:
                room = MAX_PCS_PER_DEPARTMENT - len(current)
                return _fail(f"{dname} can hold at most {MAX_PCS_PER_DEPARTMENT} PCs (room for {room} more)")
            used_ids = set(self.pcs)
            used_labels = {p["label"].lower() for p in self.pcs.values()}
            used_hosts = {p["host"] for p in current}
            slug = _slug(dname)
            planned = []
            for i in range(count):
                n = 2
                while f"{slug}-pc-{n}" in used_ids or (not name and f"{dname} PC {n}".lower() in used_labels):
                    n += 1
                pid = f"{slug}-pc-{n}"
                if name:
                    label = name if count == 1 else f"{name} {i + 1}"
                    if label.lower() in used_labels:
                        return _fail(f'A PC named "{label}" already exists')
                else:
                    label = f"{dname} PC {n}"
                host = FIRST_HOST
                while host in used_hosts:
                    host += 1
                used_ids.add(pid)
                used_labels.add(label.lower())
                used_hosts.add(host)
                planned.append({"id": pid, "label": label, "department": dname, "vlan": dept["vlan"],
                                "subnet": dept["subnet"], "gateway": dept["gateway"], "host": host, "default": False})
            for pc in planned:
                self.pcs[pc["id"]] = pc
            what = f'PC "{planned[0]["label"]}"' if count == 1 else f"{count} PCs"
            self._event(f"Added {what} to {dname} (VLAN {dept['vlan']})", "success")
            return {"success": True, "added": [self._pc_view(p) for p in planned]}

    def remove_pc(self, pc_id):
        with self._lock:
            pc = self.pcs.get(pc_id)
            if not pc:
                return _fail("Unknown PC")
            siblings = [p for p in self.pcs.values() if p["department"] == pc["department"]]
            if len(siblings) <= 1:
                return _fail(f"{pc['department']} must keep at least one PC")
            del self.pcs[pc_id]
            self.leases.pop(pc_id, None)
            self._event(f'Removed PC "{pc["label"]}" from {pc["department"]}; its lease was released', "warning")
            return {"success": True, "removed": pc_id, "label": pc["label"]}

    def reset_pcs(self):
        with self._lock:
            self._load_default_pcs()
            self.leases = {}
            self._event("PC inventory restored to the 4 default PCs", "info")
            return self.status()

    def reset(self):
        with self._lock:
            self.failures = {"dns": False, "dhcp": False, "web": False, "link": False}
            self.events = []
            self.leases = {}
            self.counters = {"connection_tests": 0, "allowed": 0, "blocked": 0, "dhcp_success": 0, "dns_success": 0}
            self._event("Simulation reset; all modeled services operational", "success")
            return self.status()

    def _event(self, message, kind="info"):
        self.events.append({"time": datetime.now().strftime("%H:%M:%S"), "event": message, "kind": kind})
        self.events = self.events[-50:]

    def status(self):
        with self._lock:
            return {
                "mode": "DEGRADED" if any(self.failures.values()) else "NORMAL",
                "failures": dict(self.failures),
                "departments": DEPARTMENTS,
                "department_list": [{"name": d["department"], "vlan": d["vlan"], "subnet": d["subnet"], "gateway": d["gateway"]} for d in DEPARTMENTS.values()],
                "pcs": [self._pc_view(p) for p in sorted(self.pcs.values(), key=lambda p: (p["vlan"], p["host"]))],
                "limits": {"max_per_department": MAX_PCS_PER_DEPARTMENT, "max_add_at_once": MAX_ADD_AT_ONCE},
                "servers": SERVERS,
                "dns_records": DNS_RECORDS,
                "leases": dict(self.leases),
                "counters": dict(self.counters),
                "recent_events": list(reversed(self.events[-12:])),
                "important_note": "Logical simulation only: no real packets are transmitted and performance metrics are not measured."
            }

    def dhcp_request(self, device):
        with self._lock:
            if device not in self.pcs:
                return {"success": False, "reason": "Unknown PC"}
            if self.failures["link"] or self.failures["dhcp"]:
                reason = "Core/trunk link unavailable" if self.failures["link"] else "Central DHCP service unavailable"
                self._event(f"DHCP failed for {device}: {reason}", "error")
                return {"success": False, "service": "DHCP", "reason": reason}
            d = self.pcs[device]
            ip = f"192.168.{d['vlan']}.{d['host']}"
            lease = {"device": device, "ip": ip, "mask": "255.255.255.0", "gateway": d["gateway"], "dns": SERVERS["dns-server"]["ip"], "exchange": ["Discover", "Offer", "Request", "ACK"]}
            self.leases[device] = lease
            self.counters["dhcp_success"] += 1
            self._event(f"DHCP DORA completed for {device}; assigned {ip}", "success")
            return {"success": True, "service": "DHCP", "lease": lease}

    def dns_lookup(self, name):
        with self._lock:
            name = (name or "").strip().lower().rstrip(".")
            if self.failures["link"] or self.failures["dns"]:
                reason = "Core/trunk link unavailable" if self.failures["link"] else "Central DNS service unavailable"
                self._event(f"DNS lookup failed for {name}: {reason}", "error")
                return {"success": False, "query": name, "reason": reason}
            ip = DNS_RECORDS.get(name)
            if ip:
                self.counters["dns_success"] += 1
                self._event(f"DNS A record {name} resolved to {ip}", "success")
                return {"success": True, "query": name, "type": "A", "answer": ip}
            self._event(f"DNS query {name}: no matching record", "warning")
            return {"success": False, "query": name, "reason": "No matching DNS A record (NXDOMAIN)"}

    def connect(self, source, destination):
        with self._lock:
            src = self.pcs.get(source)
            if not src:
                return {"success": False, "reason": "Unknown source device"}
            self.counters["connection_tests"] += 1
            dst = self.pcs.get(destination)
            if dst:
                if destination == source:
                    return self._result(False, source, destination, "Source and destination are the same device")
                if dst["vlan"] == src["vlan"]:
                    return self._result(True, source, destination, f"Same VLAN {src['vlan']}: the switch delivers this directly, no routing needed")
            if self.failures["link"]:
                return self._result(False, source, destination, "Core/trunk link unavailable")
            if dst:
                # Demonstration policy: departments may reach central services but not one another.
                return self._result(False, source, destination, "Inter-department traffic denied by example segmentation policy")
            if destination not in SERVERS:
                return self._result(False, source, destination, "Unknown destination")
            if destination == "dns-server" and self.failures["dns"]:
                return self._result(False, source, destination, "DNS service unavailable")
            if destination == "dhcp-server" and self.failures["dhcp"]:
                return self._result(False, source, destination, "DHCP service unavailable")
            if destination == "web-server" and self.failures["web"]:
                return self._result(False, source, destination, "HTTP service unavailable")
            self.counters["allowed"] += 1
            self._event(f"ALLOWED {source} -> {destination}", "success")
            return {"success": True, "source": source, "destination": destination, "destination_ip": SERVERS[destination]["ip"], "reason": "Allowed by the logical demonstration policy"}

    def _result(self, success, source, destination, reason):
        key = "allowed" if success else "blocked"
        self.counters[key] += 1
        self._event(f"{'ALLOWED' if success else 'BLOCKED'} {source} -> {destination}: {reason}", "success" if success else "warning")
        return {"success": success, "source": source, "destination": destination, "reason": reason}

    def toggle_failure(self, kind):
        with self._lock:
            if kind not in self.failures:
                raise ValueError("Failure must be dns, dhcp, web, or link")
            self.failures[kind] = not self.failures[kind]
            state = "FAILED" if self.failures[kind] else "RESTORED"
            self._event(f"{kind.upper()} {state}", "error" if self.failures[kind] else "success")
            return self.status()
