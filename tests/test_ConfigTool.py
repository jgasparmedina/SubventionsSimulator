import unittest, pickle
from PyQt5 import QtCore, QtGui, QtWidgets, QtTest

from SubventionsConfigTool import SubventionsConfigToolUI

class SubventionsConfigToolUITest (unittest.TestCase):
    def setUp(self):
        app = QtWidgets.QApplication([])
        MainWindow = QtWidgets.QMainWindow()
        ui = SubventionsConfigToolUI.Ui_MainWindow()
        ui.setupUi(MainWindow)
        ui.customUI()
        ui.setApp(app)
        MainWindow.show()
        app.setApplicationName("Subventions Config Tool")
        app.setApplicationVersion("1.0")
        app.setApplicationDisplayName("Subventions Config Tool")
        app.aboutToQuit.connect(ui.exit)
        self.configTool = ui
        f = open ("prestaciones.dat", "rb")
        attributes = pickle.load (f)
        subventions = pickle.load (f)
        f.close ()
        self.configTool.attributes = attributes
        self.configTool.subventions = subventions
        self.configTool.loadData ()

    def tearDown(self):
        pass

    def testListWidgets(self):
        self.assertEqual(self.configTool.attributesListWidget.count (), 30)
        self.assertEqual(self.configTool.subventionsListWidget.count (), 34)

    def testAttributeSelected(self):
        self.configTool.attributesListWidget.setCurrentRow(6)
        self.assertEqual(self.configTool.attributeNameField.text(), "EMANCIPADO")
        self.assertEqual(self.configTool.attributeQuestionField.toPlainText(), "¿Estás emancipado?")
        self.assertEqual(self.configTool.attributeHelpField.toPlainText(), "Si es menor de edad pero se ha independizado.")
        self.assertEqual(self.configTool.attributeTypeField.currentText(), "Sí/No")
        self.assertEqual(self.configTool.valuesTable.rowCount(), 2)
        self.assertEqual(self.configTool.valuesTable.item(0, 0).text(), "Sí")
        self.assertEqual(self.configTool.valuesTable.item(1, 0).text(), "No")

    def testAttributeSelectedWithDetails(self):
        self.configTool.attributesListWidget.setCurrentRow(16)
        self.assertEqual(self.configTool.attributeNameField.text(), "NACIONALIDAD")
        self.assertEqual(self.configTool.attributeQuestionField.toPlainText(), "Indica tu nacionalidad")
        self.assertEqual(self.configTool.attributeHelpField.toPlainText(), "")
        self.assertEqual(self.configTool.attributeTypeField.currentText(), "Lista de opciones")
        self.assertEqual(self.configTool.valuesTable.rowCount(), 4)
        self.assertEqual(self.configTool.valuesTable.item(0, 0).text(), "Española")
        self.assertEqual(self.configTool.valuesTable.item(0, 1).text(), "")
        self.assertEqual(self.configTool.valuesTable.item(1, 0).text(), "Comunitaria")
        self.assertEqual(self.configTool.valuesTable.item(1, 1).text(), "Ciudadano de la Unión Europea que ostenta la nacionalidad de cualquiera de los Estados miembros de la UE")
        self.assertEqual(self.configTool.valuesTable.item(2, 0).text(), "No comunitario")
        self.assertEqual(self.configTool.valuesTable.item(2, 1).text(), "")
        self.assertEqual(self.configTool.valuesTable.item(3, 0).text(), "Apátrida")
        self.assertEqual(self.configTool.valuesTable.item(3, 1).text(), "Persona que no tiene nacionalidad de ningún país")

    def testAttributeSelectionDisableEdition(self):
        self.configTool.attributesListWidget.setCurrentRow(6)
        self.assertFalse(self.configTool.attributeNameField.isEnabled())
        self.assertFalse(self.configTool.attributeQuestionField.isEnabled())
        self.assertFalse(self.configTool.attributeHelpField.isEnabled())
        self.assertFalse(self.configTool.attributeTypeField.isEnabled())
        self.assertFalse(self.configTool.saveAttributeButton.isEnabled())

    def testAttributeEdition(self):
        self.configTool.attributesListWidget.setCurrentRow(6)
        self.configTool.editAttributeData()
        self.assertTrue(self.configTool.attributeNameField.isEnabled())
        self.assertTrue(self.configTool.attributeQuestionField.isEnabled())
        self.assertTrue(self.configTool.attributeHelpField.isEnabled())
        self.assertTrue(self.configTool.attributeTypeField.isEnabled())
        self.assertTrue(self.configTool.saveAttributeButton.isEnabled())
        self.assertFalse(self.configTool.editAttributeButton.isEnabled())
        self.assertFalse(self.configTool.newAttributeButton.isEnabled())
        self.assertFalse(self.configTool.deleteAttributeButton.isEnabled())

    def testAttributeDataEdition(self):
        self.configTool.attributesListWidget.setCurrentRow(6)
        self.configTool.editAttributeData()
        self.configTool.attributeNameField.setText("TEST_1")
        self.configTool.saveAttributeData()
        self.assertEqual(self.configTool.attributeNameField.text(), "TEST_1")
        self.assertEqual(self.configTool.attributesListWidget.item(25).text(), "TEST_1")
        self.assertIsNone(self.configTool.attributes.get("EMANCIPADO", None))
        self.assertIsNotNone(self.configTool.attributes.get("TEST_1", None))
        attributesCombo = []
        for i in range(self.configTool.attributeComboBox.count()):
            attributesCombo.append(self.configTool.attributeComboBox.itemText(i))
        self.assertNotIn("TEST_2", attributesCombo)

    def testNewAttributeDataEdition(self):
        self.configTool.newAttributeData()
        self.assertTrue(self.configTool.saveAttributeButton.isEnabled())
        self.configTool.attributeNameField.setText("TEST_2")
        self.configTool.attributeQuestionField.setText("Question for TEST_2")
        self.configTool.attributeTypeField.setCurrentIndex(2)
        self.configTool.valuesTable.setItem(0, 0, QtWidgets.QTableWidgetItem("Value 1"))
        self.configTool.valuesTable.setItem(0, 1, QtWidgets.QTableWidgetItem("Description for Value 1"))
        self.configTool.valuesTable.setItem(0, 0, QtWidgets.QTableWidgetItem("Value 2"))
        self.configTool.valuesTable.setItem(0, 1, QtWidgets.QTableWidgetItem("Description for Value 2"))
        self.configTool.valuesTable.setItem(0, 0, QtWidgets.QTableWidgetItem("Value 3"))
        self.configTool.valuesTable.setItem(0, 1, QtWidgets.QTableWidgetItem("Description for Value 3"))
        self.configTool.saveAttributeData()
        self.assertEqual(self.configTool.attributesListWidget.item(26).text(), "TEST_2")
        self.assertIsNotNone(self.configTool.attributes.get("TEST_2", None))
        attributesCombo = []
        for i in range (self.configTool.attributeComboBox.count()):
            attributesCombo.append (self.configTool.attributeComboBox.itemText(i))
        self.assertIn("TEST_2", attributesCombo)

    def testDeleteAttribute(self):
        self.configTool.attributesListWidget.setCurrentRow(26)
        self.configTool.deleteAttributeData()
        attributes = []
        for i in range (1, self.configTool.attributesListWidget.count()):
            attributes.append(self.configTool.attributesListWidget.item(i).text())
        self.assertNotIn("TRATA", attributes)
        attributesCombo = []
        for i in range(self.configTool.attributeComboBox.count()):
            attributesCombo.append(self.configTool.attributeComboBox.itemText(i))
        self.assertNotIn("TRATA", attributesCombo)

    def testSubventionSelected(self):
        self.configTool.subventionsListWidget.setCurrentRow(5)
        self.assertEqual(self.configTool.subventionNameField.text(), "BECA EDUC. INFANTIL")
        self.assertEqual(self.configTool.subventionTitleField.toPlainText(), "BECAS DE EDUCACIÓN INFANTIL")
        self.assertEqual(self.configTool.subventionLawField.toPlainText(), "ORDEN 349/2017, de 8 de febrero, de la Consejería de Educación, Juventud y Deporte y de la Consejería de Políticas Sociales y Familia, por la que se aprueban las bases reguladoras para la concesión de becas para la escolarización en el primer ciclo de Educación ")
        self.assertEqual(self.configTool.subventionDescriptionField.toPlainText(), "Becas de Eduación Infantil de la Comunidad de Madrid")
        self.assertEqual(self.configTool.subventionLawURLField.text(), "")
        self.assertEqual(self.configTool.subventionRequestURLField.text(), "")
        self.assertEqual(self.configTool.subventionIncompatibilitiesField.toPlainText(), "Las becas concedidas al amparo de las presentes bases reguladoras son incompatiblescon otras ayudas o becas con finalidad similar, provenientes de la propia Comunidad de Madrid, de otras Administraciones Públicas, de otros entes públicos o privados o de par-ticulares nacionales o internacionales.")
        self.assertEqual(self.configTool.subventionRulesWidget.topLevelItemCount(), 5)

    def testSubventionSelectionDisableEdition(self):
        self.configTool.subventionsListWidget.setCurrentRow(5)
        self.assertFalse(self.configTool.subventionNameField.isEnabled())
        self.assertFalse(self.configTool.subventionTitleField.isEnabled())
        self.assertFalse(self.configTool.subventionLawField.isEnabled())
        self.assertFalse(self.configTool.subventionDescriptionField.isEnabled())
        self.assertFalse(self.configTool.subventionLawURLField.isEnabled())
        self.assertFalse(self.configTool.subventionRequestURLField.isEnabled())
        self.assertFalse(self.configTool.subventionIncompatibilitiesField.isEnabled())
        self.assertFalse(self.configTool.subventionRulesWidget.isEnabled())
        self.assertFalse(self.configTool.newOrConditionButton.isEnabled())
        self.assertFalse(self.configTool.newAndConditionButton.isEnabled())
        self.assertFalse(self.configTool.attributeComboBox.isEnabled())
        self.assertFalse(self.configTool.valuesComboBox.isEnabled())
        self.assertFalse(self.configTool.operatorComboBox.isEnabled())
        self.assertFalse(self.configTool.conditionValueField.isEnabled())


    def testSubventionEdition(self):
        self.configTool.subventionsListWidget.setCurrentRow(5)
        self.configTool.editSubventionData()
        self.assertTrue(self.configTool.subventionNameField.isEnabled())
        self.assertTrue(self.configTool.subventionTitleField.isEnabled())
        self.assertTrue(self.configTool.subventionLawField.isEnabled())
        self.assertTrue(self.configTool.subventionDescriptionField.isEnabled())
        self.assertTrue(self.configTool.subventionLawURLField.isEnabled())
        self.assertTrue(self.configTool.subventionRequestURLField.isEnabled())
        self.assertTrue(self.configTool.subventionIncompatibilitiesField.isEnabled())
        self.assertTrue(self.configTool.subventionRulesWidget.isEnabled())
        self.assertTrue(self.configTool.newOrConditionButton.isEnabled())
        self.assertTrue(self.configTool.newAndConditionButton.isEnabled())
        self.assertTrue(self.configTool.attributeComboBox.isEnabled())
        self.assertTrue(self.configTool.valuesComboBox.isEnabled())
        self.assertTrue(self.configTool.operatorComboBox.isEnabled())
        self.assertTrue(self.configTool.conditionValueField.isEnabled())

    def testSubventionDataEdition(self):
        self.configTool.subventionsListWidget.setCurrentRow(5)
        self.configTool.editSubventionData()
        self.configTool.subventionNameField.setText("TEST_1")
        self.configTool.saveSubventionData()
        self.assertEqual(self.configTool.subventionNameField.text(), "TEST_1")
        self.assertEqual(self.configTool.subventionsListWidget.item(31).text(), "TEST_1")
        self.assertIsNone(self.configTool.getSubventionId("BECA EDUC. INFANTIL"))
        self.assertIsNotNone(self.configTool.getSubventionId("TEST_1"))

    def testNewSubventionDataEdition(self):
        self.configTool.newSubventionData()
        self.assertTrue(self.configTool.saveSubventionButton.isEnabled())
        self.configTool.subventionNameField.setText("TEST_2")
        self.configTool.subventionTitleField.setText("Test 2")
        self.configTool.subventionDescriptionField.setText("Test 2 description")
        self.configTool.newAndCondition()
        self.configTool.subventionRulesWidget.topLevelItem(0).setSelected(True)
        self.configTool.attributeComboBox.setCurrentIndex(4)
        self.configTool.subventionValuesManager()
        self.configTool.operatorComboBox.setCurrentIndex(2)
        self.configTool.conditionValueField.setText("32")
        self.configTool.newORCondition()
        self.configTool.saveSubventionData()
        self.assertEqual(self.configTool.subventionsListWidget.item(32).text(), "TEST_2")
        self.assertIsNotNone(self.configTool.subventions.get(self.configTool.getSubventionId("TEST_2"), None))

    def testDeleteAttribute(self):
        self.configTool.subventionsListWidget.setCurrentRow(26)
        self.configTool.deleteSubventionData()
        subventions = []
        for i in range (1, self.configTool.subventionsListWidget.count()):
            subventions.append(self.configTool.subventionsListWidget.item(i).text())
        self.assertNotIn("TRATA", subventions)
