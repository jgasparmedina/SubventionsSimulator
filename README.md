# SubventionsSimulator
## About The Project

SubventionsSimulator is a tookit which provides functionalities to define public subventions and helps and to check if someone fulfill the requirements to request them.

This package has different modules:
* **SubventionsSimulator**: This module implements the different concepts (Attribute, Subventions and Conditions) and the Simulator class which implements the engine that checks if one person satisfies or not some subvention.
* **SubventionConfigTool**: A QT app client which provides capabilities to configure attributes and subventions in an user-friendly way.
* **SimulatorWeb**: A Flask App which implements a Simulator web app configured for European Anti Poverty Network (EAPN).
* **DecisionTrees**: Implementation of ID3, C4.5 and CART decision tress algorithm applied to public subventions. 
* **tests**: Unitary tests of all of those modules.

### Built With

SubventionsSimulator has been built using the following frameworks:
* [Bulma](https://bulma.io)
* [Flask](https://flask.palletsprojects.com/en/2.0.x/)

## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

To use SubventionsSimulator you will need .
* PyQt5
  ```sh
  pip install -U PyQt5
  ```
* Flask
  ```sh
  pip install -U Flask
  ```
* pandas
  ```sh
  pip install -U pandas
  ```
 

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/jgasparmedina/SubventionsSimulator.git
   ```

<!-- USAGE EXAMPLES -->
## Usage
## SubventionsSimulator
### Attribute
```python
from SubventionsSimulator import Attribute
attribute1 = Attribute.Attribute ("Age", "How old are you?", None, None, float, "Indicate your age")
attribute2 = Attribute.Attribute ("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
```
### Condition
One condition could be **simple**, **OR** or **AND**
#### Simple Condition
One single conditions is which defines one attribute, one operator and one or some values to be evaluated.
For instance:
- Attribute could be AGE
- Operator could be "="
- Values could be 32
In this example, the simple condition could understood like "AGE must to be equal to 32"

The valid operators are:
- "=": the attribute value must to be "equal" to the specified value.
- "!=":  the attribute value must to be "not equal" the specified value.
- "<":  the attribute value must to be "less than" the specified value.
- "<=":  the attribute value must to be "less or equal than" the specified value.
- ">":  the attribute value must to be "greater than" the specified value.
- ">=":  the attribute value must to be "greater or equal than" the specified value.
- "IN":  the attribute value must to be "included in" the specified list of values.
- "NOT IN":  the attribute value must to be "not included in" the specified list of values.

```python
from SubventionsSimulator import Attribute, Condition
attribute1 = Attribute.Attribute ("Age", "How old are you?", None, None, float, "Indicate your age")
condition1 = Condition.SimpleCondition (attribute1, "=", "32")```

attribute2 = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
condition2 = Condition.SimpleCondition(attribute2, "IN", ["European", "English"])
```
#### AND Condition
Represents the composition of several conditions following an AND logic.
AND condition will be True if all of the conditions are True.
```python
from SubventionsSimulator import Attribute, Condition
attribute = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
c1 = Condition.SimpleCondition(attribute, "=", "European")
c2 = Condition.SimpleCondition(attribute, "!=", "Spanish")
cAND = Condition.AND(c1, c2)
```
#### OR Condition
Represents the composition of several conditions following an OR   logic.
OR condition will be True if, at least, one of the conditions is True.
```python
from SubventionsSimulator import Attribute, Condition
attribute = Attribute.Attribute ("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
c1 = Condition.SimpleCondition (attribute, "=", "European")
c2 = Condition.SimpleCondition (attribute, "!=", "Spanish")
cOR = Condition.OR (c1, c2)
```
#### Combining conditions
All conditions can be combined generating more complex conditions
```python
from SubventionsSimulator import Attribute, Condition
attribute1 = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
attribute2 = Attribute.Attribute ("Age", "How old are you?", None, None, float, "Indicate your age")
attribute3 = Attribute.Attribute ("Civil state", "Are you married?", ['Yes', 'No'], [], bool, "Indicate your civil state")
c1 = Condition.SimpleCondition(attribute1, "IN", ["European", "English"])
c2 = Condition.SimpleCondition(attribute2, "!=", 25)
c3 = Condition.SimpleCondition(attribute3, "=", "Yes")
cOr = Condition.OR (c1, c2)
cAnd = Condition.AND(cOr, c3)
```
#### Checking conditions
Conditions can be checked in terms to determine if are satisfy or not based on provided attributes data. Attributes data must to be informed as a dict where keys are attribute names and values are their values.
```python
from SubventionsSimulator import Attribute, Condition
attribute1 = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
attribute2 = Attribute.Attribute ("Age", "How old are you?", None, None, float, "Indicate your age")
attribute3 = Attribute.Attribute ("Civil state", "Are you married?", ['Yes', 'No'], [], bool, "Indicate your civil state")
c1 = Condition.SimpleCondition(attribute1, "IN", ["European", "English"])
c2 = Condition.SimpleCondition(attribute2, "!=", 25)
c3 = Condition.SimpleCondition(attribute3, "=", "Yes")
cOr = Condition.OR (c1, c2)
cAnd = Condition.AND(cOr, c3)
values = {'Nationality' : 'English',
          'Age' : 32,
          'Civil state' : 'No'}
cOr.check (**values)
```
### Subvention
One subvention is, mainly, one set of conditions to be satisfied in terms to request it.
```python
from SubventionsSimulator import Attribute, Condition, Subvention
attribute = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
condition = Condition.SimpleCondition(attribute, "=", "Spanish")
subvention = Subvention.Subvention("Title", "Description", "Law", condition, lawURL = "url", requestURL = "requestURL", incompatibilities = "Incompatibilities")
subvention.checkCompliance (** {'Nationality' : 'Spanish'})
```
### Simulator
Simulator drives the process to get information from the conditions for all the configured subventions.
```python
from SubventionsSimulator import Attribute, Condition, Subvention, Simulator
attribute1 = Attribute.Attribute("Nationality", "What is your nationality?", ['Spanish', 'English', 'European', 'Others'], ['', '', '', 'For other countries'], list, "Indicate your nationality")
attribute2 = Attribute.Attribute("Age", "How old are you?", None, None, float, "Indicate your age")
attribute3 = Attribute.Attribute ("Civil state", "Are you married?", ['Yes', 'No'], [], bool, "Indicate your civil state")
condition1 = Condition.SimpleCondition(a, "=", "Spanish")
condition2 = Condition.SimpleCondition(a2, "<", 25)
condition3 = Condition.SimpleCondition(a3, "=", "No")
cAND = Condition.AND(condition1, condition2)
cOR = Condition.OR(condition2, condition3)
subvention1 = Subvention.Subvention("Subvention 1", "Description for subvention 1", "Law 1", cAND, lawURL = "URL 1", requestURL = "requestURL 1", incompatibilities = "Incompatibilities 1")
subvention2 = Subvention.Subvention("Subvention 2", "Description for subvention 2", "Law 2", cOR, lawURL = "URL 2", requestURL = "requestURL 2", incompatibilities = "Incompatibilities 2")
simulator = Simulator.Simulator({1: subvention1,
                                 2: subvention2})
simulator.startSimulation()
nextAttribute = simulator.getNextAttribute()
simulator.setAttributeData ("Age", 24)
nextAttribute = simulator.getNextAttribute()
simulator.setAttributeData("Civil state", "No")
nextAttribute = simulator.getNextAttribute()
simulator.setAttributeData("Nationality", "Spanish")
subventionsOk = simulator.getSubventionsOk ()
```

## License
Distributed under the [GPL v3 License](https://www.gnu.org/licenses/gpl-3.0.html). See `LICENSE` for more information.

## Contact
Project Link: [https://github.com/jgasparmedina/SubventionsSimulator](https://github.com/jgasparmedina/SubventionsSimulator)

