# Please modify the settings below according to your needs.
# These settings control the advanced Fragment (Finalmask) mechanism that gets
# applied to every config inside xray_fragment_balancer.py.

# Set to True to apply Fragment to every config in the Fragment-enabled JSON output.
# Set to False to generate that JSON without any Fragment applied (identical to the
# normal load-balanced JSON, just kept as a separate file).
FRAGMENT_ENABLED = True

# Stage 1 Fragment settings (same fields as the "Fragment" section in TCB).
# packets: which packet to target. "tlshello" means the TLS ClientHello packet.
# lengths: how many bytes each split piece should be. Example: 5,94,1
# delays: delay in milliseconds between sending each split piece. Example: 0
# max_split: maximum number of splits. 0 means no extra limit.
FRAGMENT_STAGE_1 = {
    "packets": "tlshello",
    "lengths": ["5", "94", "1"],
    "delays": ["0"],
    "max_split": "0"
}

# Set to True to also apply a second Fragment stage on top of the first one
# (this is the "Finalmask" two-layer splitting used in TCB).
FRAGMENT_STAGE_2_ENABLED = True

# Stage 2 Fragment settings (same fields as the "Stage 2" section in TCB).
# packets: "1-1" means it re-splits the very first outgoing packet again,
# regardless of its content, further breaking up Stage 1's output.
FRAGMENT_STAGE_2 = {
    "packets": "1-1",
    "lengths": ["109", "1"],
    "delays": ["1"],
    "max_split": "355"
}

# TLS fingerprint to force on every TLS/XTLS config when Fragment is enabled.
# "unsafe" matches the "Use raw fingerprint" option in TCB.
# Leave as an empty string "" to keep each config's own original fingerprint.
FRAGMENT_TLS_FINGERPRINT = "unsafe"

# Custom TLS cipher suites to force on every TLS/XTLS config when Fragment is enabled.
# Leave as an empty string "" to keep Xray's default cipher suites.
FRAGMENT_TLS_CIPHER_SUITES = "TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256:TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384:TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384:TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256:TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256:TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256:TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256:TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA:TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA:TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256:TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256"