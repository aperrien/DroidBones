from xml.etree import ElementTree
import xml.parsers.expat
import os
import re

class LayoutProcessor:
    
    def __init__(self):
        self.data = {}
        self.writer = javaCodeWriter()
        


    def importLayout(self,filename):
        try:
            tree = xml.etree.ElementTree.parse(filename)
        except (EnvironmentError,
                xml.parsers.expat.ExpatError) as err:
            print("{0}: import error: {1}".format(
                os.path.basename(sys.argv[0]),err))
            return False
        
        self.locateAllWidgets('Button',tree)
        self.locateAllWidgets('CheckBox',tree)
        self.locateAllWidgets('EditText',tree)




    def locateAllWidgets(self,widget,tree):
        for widgetElement in tree.findall(widget):
            try:
                
                widgetID = re.sub('\@\+id\/','',widgetElement.get('{http://schemas.android.com/apk/res/android}id'))
                

                self.writer.allWidgets[widgetID]=widget
                self.writer.widgetTypes.add(widget)

                    
            except (ValueError, LookupError) as err:
                print("{0} : import widget error: {1}".format(
                    os.path.basename(sys.argv[0]),err))
                return False

            
                    
    ##            for attribute in ("Button","CheckBox","RadioButton","ImageButton", "ImageButton", \
    ##                              "Gallery", "Spinner", "EditText", "AutoCompleteTextView", \
    ##                              "ProgressBar", "DigitalClock", "DatePicker", "TimePicker", \
    ##                              "AnalogClock", "TextView" ):

                                  



class javaCodeWriter:
    def __init__(self):
        self.indentLevel = 0
        self.indentString = ' '
        self.allWidgets = {}
        self.widgetTypes = set([])
        self.code = []
        pass

    def makeIndentString(self,additionalIndent):
        return ((self.indentLevel*4)+additionalIndent*4)*self.indentString
    
    def writeButtonClick(self,buttonID):

        actionSection = [''] * 3
        declareString = self.makeIndentString(0) + "final Button " + buttonID + " = (Button) findViewById(R.id." + buttonID + ");"
        eventString = self.makeIndentString(0) + buttonID + ".setOnClickListener(new View.OnClickListener() {"
        actionSection[0] = self.makeIndentString(1) + "public void onClick(View v) {"
        actionSection[1] = self.makeIndentString(2) + "// Actions for the " + buttonID + " button."
        actionSection[2] = self.makeIndentString(1) + "}"
        wrapUpString = "});"

        function = [ declareString, eventString ]
        
        for action in actionSection:
            function.append(action)
            
        function.append(wrapUpString)

        return function

    def writeEditTextEntry(self,editTextID):

        actionSection = [''] * 10
        declareString = self.makeIndentString(0) + "final EditText " + editTextID + " = (EditText) findViewById(R.id." + editTextID + ");"
        eventString = self.makeIndentString(0) + editTextID + ".setOnKeyListener(new OnKeyListener() {"
        actionSection[0] = self.makeIndentString(1) + "public boolean onKey(View v, int keyCode, KeyEvent event) {"
        actionSection[1] = self.makeIndentString(2) + '// If the event is a key-down event on the "enter" button'
        actionSection[2] = self.makeIndentString(2) + 'if ((event.getAction() == KeyEvent.ACTION_DOWN) &&'
        actionSection[3] = self.makeIndentString(3) + '(keyCode == KeyEvent.KEYCODE_ENTER)) {'
        actionSection[4] = self.makeIndentString(2) + '// Perform action on key press'
        actionSection[5] = self.makeIndentString(2) + '// Actions for ' + editTextID + ' EditText box go here.'
        actionSection[6] = self.makeIndentString(2) + 'return true;'
        actionSection[7] = self.makeIndentString(2) + '}'
        actionSection[8] = self.makeIndentString(2) + 'return false;'
        actionSection[9] = self.makeIndentString(1) + '}'
        
        wrapUpString = "});"

        function = [ declareString, eventString ]
        
        for action in actionSection:
            function.append(action)
            
        function.append(wrapUpString)

        return function


    def writeCheckBoxClick(self,checkBoxID):

        actionSection = [''] * 9
        declareString = self.makeIndentString(0) + "final CheckBox " + checkBoxID + " = (CheckBox) findViewById(R.id." + checkBoxID + ");"
        eventString = self.makeIndentString(0) + checkBoxID + ".setOnClickListener(new View.OnClickListener() {"
        actionSection[0] = self.makeIndentString(1) + "public void onClick(View v) {"
        actionSection[1] = self.makeIndentString(2) + "// Actions for the " + checkBoxID + " checkbox."
        actionSection[2] = self.makeIndentString(2) + "// Perform action on clicks, depending on whether or not it's checked"
        actionSection[3] = self.makeIndentString(2) + "if (((CheckBox) v).isChecked()) {"
        actionSection[4] = self.makeIndentString(3) + "// Checked actions"
        actionSection[5] = self.makeIndentString(2) + "} else {"
        actionSection[6] = self.makeIndentString(3) + "// Unchecked actions"
        actionSection[7] = self.makeIndentString(2) + "}"
        actionSection[8] = self.makeIndentString(1) + "}"
        
        wrapUpString = "});"

        function = [ declareString, eventString ]
        
        for action in actionSection:
            function.append(action)
            
        function.append(wrapUpString)

        return function

    def writeRadioButtonListener(self,buttonID):

        actionSection = [''] * 2
        actionSection[0] = self.makeIndentString(0) + "final RadioButton " + buttonID + "Radio = (RadioButton) findViewById(R.id." + buttonID + ");"
        actionSection[1] = self.makeIndentString(0) + buttonID + "Radio.setOnClickListener(" + buttonID + "RadioListener);"

        function = []
        
        for action in actionSection:
            function.append(action)

        return function

    def writeRadioButtonViewListener(self,radioButtonID):

        actionSection = [''] * 5
        actionSection[0] = self.makeIndentString(0) + "private OnClickListener " + radioButtonID + "RadioListener = new OnClickListener() {"
        actionSection[1] = self.makeIndentString(1) + "public void onClick(View v) {"
        actionSection[2] = self.makeIndentString(2) + "// Perform action on clicks"
        actionSection[3] = self.makeIndentString(2) + "RadioButton rb = (RadioButton) v;"
        actionSection[4] = self.makeIndentString(1) + "}"
        wrapUpString = "});"

        function = []

        for action in actionSection:
            function.append(action)
        function.append(wrapUpString)

        return function


    def writeInitializerSection(self,appName):

        startSection = [''] * 4
        startSection[0] = "import android.app.Activity;"
        startSection[1] = "import android.os.Bundle;"
        startSection[2] = "import android.view.View;"
        startSection[3] = "import android.view.View.OnClickListener;"

        for widget in self.widgetTypes:
                startSection.append("import android.widget." + widget + ";" )

        mainDeclaration = "public class " + appName + " extends Activity"

        startSection.append(mainDeclaration)
        startSection.append("{")

        return startSection

    def writeWidgetClick(self,widgetType,widgetID):
        if (widgetType == 'Button'):
            return self.writeButtonClick(widgetID)
        if (widgetType == 'EditText'):
            return self.writeEditTextEntry(widgetID)
        if (widgetType == 'CheckBox'):
            return self.writeCheckBoxClick(widgetID)

    def writeOnCreate(self):
        myCode = []
        for widgetID in self.allWidgets.keys():
            for codeLine in self.writeWidgetClick(self.allWidgets[widgetID],widgetID):
                myCode.append(codeLine)
        return myCode

    def writeOnStart(self):
        pass

    def writeOnRestart(self):
        pass

    def writeOnResume(self):
        pass

    def writeOnPause(self):
        pass

    def writeOnStop(self):
        pass

    def writeOnDestroy(self):
        pass

    def writeReceiver(self):
        pass

    def writeApp(self,appName):

        code = []

        for line in self.writeInitializerSection(appName):
            code.append(line)
            
        for line in self.writeOnCreate():
            code.append(line)

        return code