import pefile

# נתיב לקובץ ה-DLL שלך – ודאי שהוא נכון בהתאם לפרויקט שלך
pe = pefile.PE("D:/RShProject/codes/decision_logic.dll")

machine_type = pe.FILE_HEADER.Machine

arch = {
    0x14c: "32-bit (x86)",
    0x8664: "64-bit (x64)"
}.get(machine_type, f"Unknown (Machine: {hex(machine_type)})")

print("Architecture of DLL:", arch)
