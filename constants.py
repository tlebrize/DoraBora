POLICY = """
<?xml version="1.0" encoding="UTF-8"?>
<cross-domain-policy>
<site-control permitted-cross-domain-policies="all"/>
<allow-access-from domain="*" to-ports="*" secure="false"/>
<allow-http-request-headers-from domain="*" headers="*" secure="false"/>
</cross-domain-policy>"
"""

EOM = b"\n\0"
