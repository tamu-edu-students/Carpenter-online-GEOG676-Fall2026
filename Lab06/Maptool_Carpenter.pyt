# -*- coding: utf-8 -*-

import time

import arcpy


class Toolbox:
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [GraduatedColorsRenderer]


class GraduatedColorsRenderer:
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "graduatedcolor"
        self.description = "create a graduated colored map based on a specific attribute of a layer"
        self.canRunInBackground = False
        self.category = "MapTools"

    
    def getParameterInfo(self):
        """Define the tool parameters."""
        #original project name
        param0 = arcpy.Parameter(
            displayName= "Input ArcGIS Pro Project Name",
            name="aprxInputName",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )
       
    #which layer you want to clarify to create a color map
        param1 = arcpy.Parameter(
            displayName="Layer to Classify",
            name="LayertoClassify",
            datatype="GPLayer",
            parameterType="Required",
            direction="Input"
        )

    #output folder location
        param2 = arcpy.Parameter(
            displayName="Output Location",
            name="OutputLocation",
            datatype="DEFolder",
            direction="Input"
        )

    #output project name
        param3 = arcpy.Parameter(
            displayName="Output Project Name",
            name="OutputProjectName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        params = [param0, param1, param2, param3]
        return params
  

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        # Define Progressor Variables
        readTime = 3 #the time for users to read the progress
        start = 0 #beginning position of the progressor
        max = 100 #end position
        step = 33 #the progress interval to move the progessor along

        #Setup Progressor
        arcpy.SetProgressor("step", "Validating Project File...", start, max, step)
        time.sleep(readTime) #pause the execution for 2.5 seconds

        #Add Mesaage to the Results Pane
        arcpy.AddMessage("Validating Project File...")

        #Project file
        project = arcpy.mp.ArcGISProject(parameters[0].valueAsText)

        #Grabs the firest instance of a map from the .aprx
        campus = project.listMaps('Map')[0]

        #increment progressor
        arcpy.SetProgressorPosition(start + step)
        arcpy.SetProgressorLabel("Finding your map layer... ")
        time.sleep(readTime)
        arcpy.AddMessage("Finding your map layer...")

        #Loop through the layers of the map
        for layer in campus.listLayers():
            #Check if the layer is a feature layer
            if layer.isFeatureLayer:
                #Copy the layer's symbology
                symbology = layer.symbology
                #Make sure the symbology has renderer attribute
                if hasattr(symbology, "renderer"):
                    #Check layer name
                    if layer.name == parameters[1].valueAsText: #check if the layer name match the input layer

                        #increment progressor
                        arcpy.SetProgressorPosition(start + step * 2) 
                        arcpy.SetProgressorLabel("Calculating and classifying...")
                        time.sleep(readTime)
                        arcpy.AddMessage("Calculating and classifying...")

                        #update the copy's rendere to "Graduated Colors Renderer"
                        symbology.updateRenderer('GraduatedColorsRenderer')

                        #Tell arcpy which field we want to base our chloropleth off of
                        symbology.renderer.classificationField = "Shape_Area"

                        #Set how many classes we'll have for the map
                        symbology.renderer.breakCount = 5

                        #Set color ramp
                        symbology.renderer.colorRamp = project.listColorRamps('Oranges (5 Classes)')[0]

                        #Set the layer's actual symbology equal to the copy's
                        layer.symbology = symbology

                        arcpy.AddMessage("Finish Generating Layer...")
                    else:
                        print("NO layers found")

        #Increment progressor 
        arcpy.SetProgressorPosition(start + step * 3)
        arcpy.SetProgressorLabel("Saving...")
        time.sleep(readTime)
        arcpy.AddMessage("Saving...")

        project.saveACopy(parameters[2].valueAsText + "\\" + parameters[3].valueAsText + ".aprx")
        #Param 2 is the folder location and param 3 is the name of the new project
        return

            




        # Get the layer to classify by name
        layer_to_classify = map_obj.listLayers(LayertoClassify)[0]

        # Create a graduated color renderer for the layer based on a specific attribute
        renderer = arcpy.mp.GraduatedColorsRenderer(layer_to_classify, "attribute_name", 5)

        # Apply the renderer to the layer
        layer_to_classify.symbology = renderer

        # Save the modified project to the output location with the specified name
        output_project_path = f"{OutputLocation}/{OutputProjectName}.aprx"
        aprx.saveACopy(output_project_path)

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
