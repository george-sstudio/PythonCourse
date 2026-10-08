"""
MODULE 09 - Exercise 2: a Processing tool "Buffer in metres (safe)"

Fill the three TODOs in processAlgorithm. Test it with ex09_2_test_tool.py,
THEN install it.

Install: Processing Toolbox > Python icon > "Add Script to Toolbox..." and pick
this file. The tool appears under Scripts > PythonCourse.

What it does: buffers any vector layer by a distance in METRES, whatever the
layer's CRS. It reprojects each feature's layer to a local Azimuthal
Equidistant CRS centred on the layer, buffers there, and reprojects back.
"""
import processing
from qgis.core import (Qgis, QgsCoordinateReferenceSystem, QgsCoordinateTransform,
                       QgsFeatureSink, QgsProcessingAlgorithm, QgsProcessingException,
                       QgsProcessingUtils,
                       QgsProcessingParameterBoolean, QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFeatureSource, QgsProcessingParameterNumber)


class SafeBufferAlgorithm(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    DISTANCE = "DISTANCE"
    DISSOLVE = "DISSOLVE"
    OUTPUT = "OUTPUT"

    # --- identity: how the tool is listed --------------------------------------
    def name(self):
        return "safebuffer"                       # id becomes  script:safebuffer

    def displayName(self):
        return "Buffer in metres (safe)"

    def group(self):
        return "PythonCourse"

    def groupId(self):
        return "pythoncourse"

    def shortHelpString(self):
        return ("Buffers features by a distance in metres, even when the layer is in "
                "degrees (e.g. EPSG:4326). Uses a local azimuthal equidistant CRS "
                "centred on the layer, then returns the result in the input CRS.")

    def createInstance(self):
        return SafeBufferAlgorithm()

    # --- inputs and outputs ------------------------------------------------------
    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSource(
            self.INPUT, "Input layer", [Qgis.ProcessingSourceType.VectorAnyGeometry]))
        self.addParameter(QgsProcessingParameterNumber(
            self.DISTANCE, "Distance (metres)", Qgis.ProcessingNumberParameterType.Double,
            defaultValue=1000, minValue=0))
        self.addParameter(QgsProcessingParameterBoolean(
            self.DISSOLVE, "Dissolve result", defaultValue=False))
        self.addParameter(QgsProcessingParameterFeatureSink(
            self.OUTPUT, "Buffered", Qgis.ProcessingSourceType.VectorPolygon))

    # --- the work ------------------------------------------------------------------
    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)
        if source is None:
            raise QgsProcessingException("Invalid input layer")
        distance = self.parameterAsDouble(parameters, self.DISTANCE, context)
        dissolve = self.parameterAsBoolean(parameters, self.DISSOLVE, context)

        # a local CRS in metres, centred on the layer
        to_wgs = source.sourceCrs()
        extent = source.sourceExtent()
        if not to_wgs.isGeographic():
            t = QgsCoordinateTransform(to_wgs, QgsCoordinateReferenceSystem("EPSG:4326"),
                                       context.transformContext())
            extent = t.transformBoundingBox(extent)
        lon, lat = extent.center().x(), extent.center().y()
        local = QgsCoordinateReferenceSystem.fromProj(
            f"+proj=aeqd +lat_0={lat:.6f} +lon_0={lon:.6f} +datum=WGS84 +units=m +no_defs")
        feedback.pushInfo(f"Buffering by {distance:g} m in a local CRS centred on "
                          f"{lat:.2f}, {lon:.2f}")

        # TODO 1: step1 = processing.run("native:reprojectlayer", {INPUT: parameters[self.INPUT],
        #         TARGET_CRS: local, OUTPUT: "TEMPORARY_OUTPUT"},
        #         context=context, feedback=feedback, is_child_algorithm=True)["OUTPUT"]
        #         then: if feedback.isCanceled(): return {}

        # TODO 2: step2 = native:buffer on step1 with DISTANCE distance, SEGMENTS 16,
        #         DISSOLVE dissolve (same context/feedback/is_child_algorithm)

        # TODO 3: back = native:reprojectlayer of step2 to source.sourceCrs()
        back = None
        if back is None:
            raise QgsProcessingException("TODO 1-3 in processAlgorithm are not done yet")

        buffered = QgsProcessingUtils.mapLayerFromString(back, context)

        # write the features into OUR output ("sink"), so the tool works with any
        # output the user picks: temporary layer, GeoPackage, shapefile...
        sink, dest_id = self.parameterAsSink(parameters, self.OUTPUT, context,
                                             buffered.fields(), buffered.wkbType(),
                                             source.sourceCrs())
        for feature in buffered.getFeatures():
            sink.addFeature(feature, QgsFeatureSink.Flag.FastInsert)
        feedback.setProgress(100)
        return {self.OUTPUT: dest_id}
