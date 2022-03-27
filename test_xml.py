from xml.dom import minidom
root = minidom.Document()

xml = root.createElement("Transaction")
xml.setAttribute("Name", "AIImageInfo")
root.appendChild(xml)

logPointChildTag = root.createElement("LogPoint")
logPointChildTxt = root.createTextNode("123")
logPointChildTag.appendChild(logPointChildTxt)

wwwPointChildTag = root.createElement("wwwPoint")
wwwPointChildTxt = root.createTextNode("456")
wwwPointChildTag.appendChild(wwwPointChildTxt)

xml.appendChild(logPointChildTag)
xml.appendChild(wwwPointChildTag)



xml_str = root.toprettyxml(indent="\t")
save_path_file = "gfg.xml"
with open(save_path_file, "w") as f:
    f.write(xml_str)
