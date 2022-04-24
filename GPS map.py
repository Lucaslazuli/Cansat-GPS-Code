import serial
ser = serial.Serial('com3', 115200) #verander "com3" naar de juiste naam van seriele poort.
path = ""
# lat = []
# long = []

def getSerialText():
    ser_bytes = ser.readline().decode('utf-8').strip('\r\n')     # ser_bytes = rauwe tekst van 1 lijntje op de seriële monitor
    meting = ser_bytes.split(",")                                   # vb: als ser_bytes = "5890 4.98" dan is meting = ['5890', '4.98']
    return meting

def convertToDd(angle):
    angle = float(angle)
    degrees = angle // 100
    minutes = angle % 100

    decimalDeg = degrees + minutes / 60
    return decimalDeg

while True:
    gpsData = getSerialText()
    # print(gpsData)

    if gpsData[0] == '$GPRMC':
        if gpsData[2] == 'A':
            lon = str(convertToDd(gpsData[5]))
            lat = str(convertToDd(gpsData[3]))
            alt = "0"
            path += lon + "," + lat + "," + alt + "\n"
            with open("position.kml", "w") as pos:
                # pos.write("%s, %s\n" % (gpsData[3], gpsData[5]))
                pos.write("""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Paths</name>
    <description>Examples of paths. Note that the tessellate tag is by default
      set to 0. If you want to create tessellated lines, they must be authored
      (or edited) directly in KML.</description>
    <Style id="yellowLineGreenPoly">
      <LineStyle>
        <color>7f00ffff</color>
        <width>4</width>
      </LineStyle>
    </Style>
    <Placemark>
      <name>Absolute Extruded</name>
      <description>Transparent green wall with yellow outlines</description>
      <styleUrl>#yellowLineGreenPoly</styleUrl>
      <LineString>
        <coordinates>%s</coordinates>
      </LineString>
    </Placemark>
  </Document>
</kml>""" % (path))
                print("position updated")
    # except ValueError:
    #     pass
    # except IndexError:
    #     pass
