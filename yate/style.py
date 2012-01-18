class Style:
  def __init__(self, name, fore, back, fontStyle):
    self.name = name
    self.fore = fore
    self.back = back
    self.fontStyle = fontStyle

  def GetStyleString(self):
    styles = []

    if self.fore:
      styles.append("fore:%s" % (self.fore))

    if self.back:
      styles.append("back:%s" % (self.back))

    if self.fontStyle:
      styles.append("%s" % (self.fontStyle))

    return ",".join(styles)

  def __repr__(self):
    return self.GetStyleString();

if __name__ == "__main__":
  s = Style("algo", "black", "blue", "italic")
  print s.GetStyleString()
