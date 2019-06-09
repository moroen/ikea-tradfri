[Unit]
Description=IKEA Tradfri COAP-adapter

[Service]
Type=simple
ExecStart=$tradfri server 

User=$user
Group=$group

Restart=always

[Install]
WantedBy=multi-user.target
