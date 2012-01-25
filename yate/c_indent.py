class CIndent:
  def __init__(self, editor):
    self.editor = editor

  def AutoIndent(self, char):
    if char == ord('\n'):
      current = self.editor.GetCurrentLine()
      prevLine = self.editor.GetLineRaw(current - 1)
      indent = self.editor.GetLineIndentation(current - 1)

      if len(prevLine.strip()) > 0:
        prevIndent = indent / self.editor.GetTabWidth()

        if prevLine.strip()[-1] == '{' or prevLine.strip()[-1] == '(':
          indent += self.editor.GetTabWidth()
        elif prevLine.strip()[-1] == '}' or prevLine.strip()[-1] == ')':
          if indent > self.editor.GetTabWidth():
            indent -= self.editor.GetTabWidth()

      self.editor.SetLineIndentation(current, indent)
      self.editor.LineEnd()
    elif char == ord('}') or char == ord(')'):
      opposites = {
        ord('}') : '{',
        ord(')') : '(',
      }

      current = self.editor.GetCurrentLine()

      # try to auto-indent ending braces
      if current > 0:
        prevLine = self.editor.GetLineRaw(current - 1)
        indent = self.editor.GetLineIndentation(current)

        if len(prevLine.strip()) > 0:
          if prevLine.strip()[-1] != opposites[char]:
            prevIndent = self.editor.GetLineIndentation(current - 1)

            # if has same indentation needs to decrese
            if prevIndent == indent:
              indent -= self.editor.GetTabWidth()
              self.editor.SetLineIndentation(current, indent)

