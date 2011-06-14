from LayoutParser import LayoutProcessor,javaCodeWriter


proc = LayoutProcessor()

proc.importLayout("Sample02.xml")

code = proc.writer.writeApp('test_app')

for l in code:
	print l
