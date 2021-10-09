# callflow
Binary function flow analyzer

plugins will:
* get a list of functions
* go through the function and find everything they call
* send data to server, which will store that data in the neo4j db

---

`dst_sym` may be empty

```json
{
    "filename": "pwn1",
    "sha256": "aaaaaa1111111135532235235...",
    "src": "ida",
    "functions": [
        {
            "name": "main",
            "va": "0x401020",
            "calls": [
                {
                    "src_va": "0x401034",
                    "dst_va": "0x402397",
                    "dst_sym": "print_name"
                },
                {
                    "src_va": "0x401034",
                    "dst_va": "0x402397",
                    "dst_sym": "print_name"
                }
            ]
        },
        {
            "name": "get_input",
            "va": "0x401090",
            "calls": [
                {
                    "src_va": "0x401034",
                    "dst_va": "0x402397",
                    "dst_sym": "print_name"
                },
                {
                    "src_va": "0x401034",
                    "dst_va": "0x402397",
                    "dst_sym": "print_name"
                }
            ]
        }
    ]
}
```