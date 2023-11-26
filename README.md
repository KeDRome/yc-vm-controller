# yc-vm-controller
Controller for VM hosted on yandex cloud

---

Yandex cloud let you buy a VM (but VM may be stopped in some times) for lower price.

This tool let you setup automatic monitor for yours lowcost VMs

1. Input OAuth token in config.yml:
2. Input as list VMs and tool will be monitor targets (or just input `all`, then all VMs will be).
3. Then move config in "safe place":
    ```bash
    mv config.yml .config.yml
    ```
4. Run it where are you want, with:
    ```bash
    ./main.py
    ```

Thas all folks!
