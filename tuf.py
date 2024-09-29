tuf = [
    "Intel Core@TW i7-14900K",
    "NVIDIA GEFORCE RTX 4080 SURPEER",
    "ADATA XPG DDR-5 6000MHZ 64GB(32GB*2)",
    "Circult T500 2TB(1TB*2)",
    "TUF GAMING GT302"
]

with open("TUF.txt", "w") as file:
    for title in tuf:
        file.write(title + "\n")


