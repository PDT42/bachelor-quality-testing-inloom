# Test Daten Analyse

## Test Daten
Der Ordner ``student-solutions`` enthält studentische Lösungen zu drei verschiedenen Aufgaben.
Für jede der Aufgaben steht die Expertenlösung, sowie Inlooms Auswertung der Expertenlösung zur
Verfügung. Für jede der Lösungen steht die in ein Eclipse kompatibles Format übersetzte 
studentische Lösung, sowie die von Inloom erstellten Evaluationen des studentischen Modells.

> #### ***Note***
> Es wäre auf jeden Fall gut, zusätzlich Beispiele von manuellen Korrekturen analysieren zu 
> können. Es ist wichtig zu untersuchen, welche Daten sich mit welchem Aufwand aus solchen
> auslesen lassen könnten und ob eine gänzliche Digitalisierung realistisch ist.

# INLOOM AutoEval Format
``` XML
<!ELEMENT TestResult (TestData, Results, ResultPoints)>

<!ELEMENT TestData (RuleMode, TestModel)>

<!ELEMENT ExpertModel EMPTY>
<!ATTLIST ExpertModel id CDATA #REQUIRED>  // Id of the Expert Model used for reference

<!ELEMENT TestModel EMPTY>
<!ATTLIST TestModel id CDATA #REQUIRED> // Id of the Evaluated Model

<!ELEMENT MetaModel EMPTY>
<!ATTLIST MetaModel type CDATA #REQUIRED>

<!ELEMENT MCSIdentifier EMPTY>
<!ATTLIST MCSIdentifier id CDATA #REQUIRED>

<!ELEMENT MCSVersion EMPTY>
<!ATTLIST MCSVersion value CDATA #REQUIRED>


<!ELEMENT Results (CResult)>  // List of Results

<!ELEMENT CResult (TestObject, RuleObject, RuleSet, Rule, Category, Points, Msg)>  // Container

<!ELEMENT ExpertObject (#PCDATA)>  // Name/Label of matched element in expert solution
<!ELEMENT ExpertType (#PCDATA)>  // Type of element in expert solution
<!ELEMENT TestObject (#PCDATA)>  // Name/Label of matched element in student solution
<!ELEMENT TestType (#PCDATA)>  // Type if the mateched element in student solution
<!ELEMENT Rule (#PCDATA)>  // Id of the Rule/Constraint (unique within Rule/Constraint-Group)
<!ELEMENT Category (#PCDATA)>  // Assigned Flag
<!ELEMENT Points (#PCDATA)>  // Awarded Points
<!ELEMENT MSG (#PCDATA)>  // Feedback Message

<!ELEMENT ResultPoints (ModelPoints, TestPoints)>  // Container

<!ELEMENT ModelPoints (#PCDATA)>  // Possible Points
<!ELEMENT TestPoints (#PCDATA)>  // Awarded Points
```

## Test Daten Satz
In dem Gespräch vom 30.10.2020 ist klar geworden, dass eine AutoEval von INLOOMS Bewertungen 
mittelfristig wohl noch nicht gänzlich auf digitalisierten Optimalkorrekturen wird beruhen 
könnnen. Desshalb sollte der Daten Satz zum Speichern statistischer Analyse Werte prioritäsiert 
werden. Ich denke, dass es leicht möglich sein sollte, ein einheitliches Datenformat für beiden 
Arten von Testdatensätzen zu erstellen. Alle Werte die ein "statistischer Datensatz" enthalten 
könnte, könnten aus den komplexeren Datensätzen vollständig digitalisierter Optimalkorrekturen, 
abgeleitet werden.

Als erstes möchte ich eine Liste der statistischen Werte erstellen, von denen ich denke, dass 
sie sowohl aus *manEval* als auch aus *autoEval* abgeleitet werden. Ich mache das aktiv *vor* 
der Literaturrecherche zum Thema Inter-Rater-Reliability Statistics, weil ich keine verfügbaren 
Werte anhand einer gewählten Statistik suchen, sondern eine Statistik anhand der am besten 
verfügbaren Werte wählen möchte.

> #### **Note**
> Es ist natürlich notwendig und sinnvoll, die Liste der verfügbaren Werte nachträglich zu 
> ergänzen, sollten Statistiken Werte erforden, die ebenfalls leicht auslesbar sind, aber bei 
> der initialen Analyse nicht bedacht wurden.

> #### **Note**
> Zu diesem Schritt wäre es gut die Liste der Constraints, sowie alle schriflichen 
> Korrekturhilfen , die den Tutoren bei der Korrektur zur Verfügung stehen, zu kennen. Wofür 
> gibt der Tutor bei der manuellen Korrektur? Welche *abzählbaren* Markierungen hinterlässt er 
> in der auswertbaren manuellen Korrektur?

> #### **Question**
> In welcher *genauen* Relation stehen Flags und Punkte? Gibt es ein Schema?

### Zur Auswertung verfügbare Werte
    
1. *TestPoints*
        
    Offensichtlich kann die resultiernde Gesamtpunktzahl leicht aus beiden Eval erfasst werden. 
    Anhand der *TestPoints* kann eine grobe Einschätzung der Bewertungsqualität vorgenommen 
    werden.

2. *Anzahl verschiedener gematchter Elemente*

    Die Anzahl der verschiedenen in verschiedenen *CResult*-s gefundenen *TestElement*s. Anhand 
    dieses Wertes kann eine Aussage darüber getroffen werden, ob INLOOM und Tutor in ihren 
    Bewertungen eine unterschiedliche Anzahl von Elementen bedacht hat.

3. *Punkte pro gematches Element*

    Punkte, die von Constraints und manuellem Prüfer pro gematchetem Element vergeben wurden. 
    Dieser Wert ist effektiv eine direkt feingranularere Darstellung von Wert 1. Anhand dieses 
    Wertes liese sich eine Aussage über die Bewertungsqauliät im Kontext bestimmter Elemente 
    treffen. Außerdem könnte aus diesem Wert eine Punkte pro Elementtyp Statistik ableiten 
    lassen, die eine Einschätzung über den Umfang des Problems, welches die Abweichung 
    verursacht, erlauben würde.

4. *Anzahl gefundener Elementmatches*

    Wie viele verschiedene Elemente wurden mit einander gematcht. Dieser Wert würde eine Aussage 
    über INLOOMS matching Qualiät zulassen und könnte einen Überblick darüber verschaffen, wie 
    aussagekräftig weiterführende Testergebnisse sind. Eine starke oder konstante Abweichung in 
    der Anzahl gefundener Elementmatches, könnte zu der Vermutung führen, dass die beiden Evals 
    auf unterschiedlichen Bewertungs-/Matchingschemata beruhen.

5. 

### Mögliche Datenstruktur für Test Datensätze in der Suite
Grundsätzlich halte ich es für sinnvoll die in den CResult XML verwendete Datenstruktur zu 
replizieren und um die erfassten Werte zur statistischen Weiterverwendung hinzuzufügen.

## Inter Rater Reliability (IRR)
Wikipedia definiert IRR als: Grad der Übereinstimmung zwischen Bewertenden, beziehungsweise, als 
Wert, der eine Aussage darüber zulässt, wie homogen die Bewertungen von zwei (oder mehreren) 
Bewertern sind. Der Wert wird als Statistik über ein Set von mehreren Bewertungen berechnet und 
dient nicht dem direkten Vergleich von manEval mit autoEval.

> #### **Note**
> Ich bin mir nicht länger sicher, ob IRR in diesem Fall wirklich sinnvoll sind. Alle diese 
> Werte dienen eher der Bewertung von *Kategorisierungen* als von *Bewertungen*. Also einer
> *Bewertung* auf einer nominal Scale. Eine Solche liegt im Fall von INLOOM aber im Grunde ja 
> nicht vor. Der Unterschied zwischen den Bewertungen ist durchaus quantifizierbar, das Problem 
> liegt also nicht bei der Verwendung eines klassischen Verhältnisses, sondern im Detaillevel 
> der bisher erfassten und verglichenen Werte. Es ist zu befürchten, dass ein Verzicht auf die 
> nummerische Differenz als Referenzwert (Unterschied zwischen Gesamtpunktzahlen der Bewertungen)
> zu einem schlechteren Ergebnis führen könnte, als wenn man sie in Betracht zieht.

### Cohens Kappa
Die wohl prominenteste unter den IRR ist Cohens Kappa. Cohens Kappa tauchte bei meiner Recherche 
*mit Abstand* am häufigsten als Begriff auf. Einige der anderen IRR, erwähnen Cohens Kappa als 
zugrundeliegende oder zumindest ähnliche Methode. [Cohen] beschreibt sein Kappa als "[...]
Proportion of agreement, after chance agreement is removed from consideration." Der Wert beruht 
auf zwei Verhältnissen, angegeben als float zwischen 0 und 1: Der erfassten Übereinstimmung 
(*agree_pct*) und der zu erwartenden zufälligen Übereinstimmung (*chance_agree_pct*). 

Zur Berechnung von agree_pct, wird die Anzahl der *Fälle*, in denen die untersuchten Bewertungen 
übereinstimmen aufaddiert und durch die gesamt Anzahl der *Fälle* geteilt. Die 
*chance_agree_pct*, also der Wahrscheinlichkeit, dass die untersuchten Bewertugen zufällig 
übereinstimmen, ergibt sich als Produkt der Wahrscheinlichkeiten, dass die Bewerter 
übereinstimmen. 

Cohens Kappa lässt lediglich den Vergleich von *zwei* Bewertern auf einmal zu. 

### Scott' Pi
Scott's Pi funktioniert im wesentlich genauso wie Cohens Kappa, zieht jedoch nicht in Betracht, 
dass unterschiedliche Rater unterschiedliche zufällige Bewertungen abgeben könnten. Stattdessen 
wird ein gemeinsamer Wert für die zufällige Verteilung von Kategorisierungen verwendet.

Scott's Pi lässt lediglich den Vergleich von *zwei* Bewertern auf einmal zu.

### Fleiss Kappa
Weiterentwicklung von Scott's Pi, welche die Möglichkeit bietet mehr als zwei Marker 
gleichzeitig zu vergleichen.

### Informedness
Weiterentwicklung von Precision und Recall, welche nicht nur Positives, sondern auch Negatives 
in Betracht zieht. 
