import os, plistlib
datos = {
    "method": "app-store",
    "teamID": os.environ["TEAM_ID"],
    "signingStyle": "manual",
    "uploadSymbols": True,
    "provisioningProfiles": {"org.collectoholic.museo": os.environ["PERFIL_NOMBRE"]},
}
with open("ExportOptions.plist", "wb") as f:
    plistlib.dump(datos, f)
print("ExportOptions.plist creado")
