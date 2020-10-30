# Problemanalyse

## Prozess
Ich stelle mir den Prozess zur Erstellung neuer Constraints folgendermaßen vor:
Ein Instruktor hat eine neue (Modellierungs-)Aufgabe erstellt, außerdem die 
Optimallösung für besagte Aufgabe. Es werden zur Aufgabe passende "Aufgaben Constraints"
erstellt, also Constraints die INLOOM nur zur Bewertung _dieser_ Aufgabe verwenden soll. 
Im Gegensatz zu "Globalen Constraints" die bei der Bewertung _jeder_ Aufgabe zum Einsatz 
kommen. 

> #### Question
> An dieser Stelle bin ich mir nicht sicher, ob die Arbeit des "Leiheninstruktors"endet,
> oder ob er noch weiter beteiligt ist. Hat er einen Anteil an der Erstellung dieser
> "Aufgaben Constraints", oder übernimmt auch diesen Teil schon der "Profi Instruktor"?

INLOOM geht nun so vor, dass es auf der Basis von "Constraint Templates", für alle, im Modell
enthaltenen Elemente, (etwa so wie bei einem Jinja-Template) "Instanzen" der Constraints
generiert.

> #### Note
> Wie genau diese Constraints zusammen kommen/zusammengesetzt werden/in Git 
> verwaltet werden, spielt im Kontext meiner Aufgabe denke ich höchstens eine
> untergeordnete Rolle.

Die erstellte Aufgabe wird in der Lehre eingesetzt. Die Studenten generieren Modelle, die 
mit dem Experten Modell verglichen werden können. Es entsteht also ein "Ist"-Datensatz.

Mit der vom Instruktor erstellten Optimallösung existiert bereits ein "Soll"-Datensatz. 
Aus dem "Soll"-Datensatz wurde mit Hilfe von "Constraint Templates" ein bestimmtes Set 
von "Constraint Instanzen" (_Constraints_) generiert. Jedes der Constraints im Set wird 
jetzt auf den "Ist"-Datensatz (studentisches _Modell_) angewendet. 
Für jedes überprüfte Modell wird ein Output XML File generiert, in dem die Resultate aller
angewendeten Constraints festgehalten werden (Hamann Thesis 3.6.4).

### Format des XML Result Files


> Das in der Thesis spezifizierte DTD ist nicht länger aktuell. Ich muss das gleiche auf jeden
> nochmal für die aktuelle XML Spezifikation machen und überprüfen ob meine Überlegungen dafür
> immernoch gelten.

> Warum die Anzahl der Tries im _name_ des TestModels persistieren, anstatt in einem eigenen 
> Element?

``` XML
<!ELEMENT TestResult (TestData, Results, ResultPoints)>

<!ELEMENT TestData (RuleModel, TestModel)>
<!ELEMENT RuleModel EMPTY>
<!ATTLIST RuleModel name CDATA #REQUIRED>  // Id of the Expert Model
<!ELEMENT TestModel EMPTY>
<!ATTLIST TestModel name CDATA #REQUIRED> // Id of the Student Model

<!ELEMENT Results (Result)>  // List of Results
<!ELEMENT Result (TestObject, RuleObject, RuleSet, Rule, Category, Points, Msg)>  // Container
<!ELEMENT TestObject (#PCDATA)>  // Name/Label of matched Element in Student Solution
<!ELEMENT RuleObject (#PCDATA)>  // Name/Label of matched Element in Expert Solution
<!ELEMENT RuleSet (#PCDATA)>  // Id of Rule/Constraint-Group
<!ELEMENT Rule (#PCDATA)>  // Id of the Rule/Constraint (unique within Rule/Constraint-Group)
<!ELEMENT Category (#PCDATA)>  // Assigned Flag
<!ELEMENT Points (#PCDATA)>  // Awarded Points
<!ELEMENT MSG (#PCDATA)>  // Feedback Message

<!ELEMENT ResultPoints (ModelPoints, TestPoints)>  // Container
<!ELEMENT ModelPoints (#PCDATA)>  // Possible Points
<!ELEMENT TestPoints (#PCDATA)>  // Awarded Points
```

_Category_ kann eine der folgenden Flags enthalten:
* __Correct__: Volle Punktzahl auf Matching von Element.
* __Warning__: Suboptimal (? Trotzdem volle Punktzahl ?).
* __Error__: Verringerte Punktzahl - klarer Fehler, aber kein Totalausfall.
* __Missing/Wrong__: Keine Punkte - Totalausfall.
* __Info__: Linting Stuff.

### Lernprozess
Beim Einführen neuer Aufgaben in INLOOM, ist es notwendig, aus den Fehlern /Lösungen der 
Studenten zu lernen. Das bedeutet, dass wenn das System bei der Bewertung einen Fehler macht 
(bei einer neuen Aufgabe vermutlich, weil Es "es nicht besser weiß"), der Instruktor neue 
Constraints hinzufügen muss, die das System in die Lage versetzen den gleichen Fehler bei der 
nächsten Bewertung nicht wieder zu machen. Es findet also unausweichlich ein "Lernprozess" im 
System statt. Ob es sich bei den neu hinzugefügten Constraints um globale oder 
aufgabenspezifische Constraints handelt, ist dabei im Grunde egal.

Damit der beschriebene Lernprozess stattfinden kann, muss der Instruktor jedoch erst einmal in 
der Laage sein, nachvollziehen zu können, dass das System einen Fehler bei der Bewertung gemacht 
hat. An dieser Stelle wird der Bedarf für eine Testsuite klar. Durch inkrementelles Hinzufügen
neuer Constraints, wird INLOOM immer besser darin Aufgaben (bzw. bestimmte Aufgaben) zu bewerten.
Die Testsuite dient primär dazu dem Instruktor zu vermitteln, dass offenbar Constraints fehlen
(Weil die Bewertung nicht seinen Ansprüchen genügt) und sekundär dazu den Instruktor bei der 
Erstellung neuer Constraints zu unterstützen, indem sie ihm als Abkürzung zu möglichen 
Fehlerquellen dient. 

> #### Note
> Außerdem ist natürlich denkbar, dass Constraints zu falschen Resultaten kommen, also zwar in 
> den richtigen Fällen angewendet werden, aber nicht das korrekte Category Flag (oder Feedback, 
> etc.) vergeben. Auf solche Fehler zu testen sehe ich eher in der Verantwortung von Unit Tests, 
> als in Der der zu erstellenden Testsuite, deren Zweck es sein soll, die automatische Bewertung 
> als Ganzes zu überprüfen.

## Anforderungen des Instruktors
Der Instruktor hat ein natürliches Interesse daran zu überprüfen, ob die, automatisch durch
INLOOM vorgenommene, Bewertung der studentischen Modelle seinen Ansprüchen genügt. Im Endeffekt 
überlässt der Instruktor seine Arbeit einem Programm und muss dessen Ergebniss/Bewertung 
verantworten. Er stellt sich also die übergeordnete Frage:  ``"Kann ich mich darauf verlassen, 
dass das Programm meinen Job mindestens genauso gut macht wie ich?"`` Er stellt also die 
Qualität von INLOOMs Arbeit in Frage. 

> #### Note
> Dieses Szenario beschreibt nicht exakt den Usecase von INLOOM. Bei INLOOM ist, so wie man
> das von INLOOP kennt (wenn ich das richtig verstanden habe) wesentlich weniger/gar kein
> Involvement des Instruktors geplant. Die Fragestellung bleibt aber die gleiche, egal ob ein
> einzelner Instruktor sie sich stellt, oder der Lehrverantwortliche der Veranstaltung SWT1.
> __Es sollte keinen Grund geben, die von INLOOM vorgenommene Bewertung anzuzweifeln.__

> Im letzten Meeting (12.10.2020) wurde die Aufgabe formuliert eine Möglichkeit zu finden
> die Qualität der durch INLOOM vorgenommenen Bewertung zu Quantifizieren.

[Bian] und [Striewe] verwenden als Referenzwert zur Evaluation der von ihren Systemen 
produzierten Bewertungen, die endgültige automatisch generierte Note und vergleichen sie mit der 
Note, die ein händischer Kontrolleur auf das selbe Modell vergeben hat. 

> Note und Gesamtpunktzahl können in diesem Kontext praktisch gleichgesetzt werden. Es gibt zwar 
> einen geringen Unterschied, weil die Zuordnung zwischen Punkten und Gesamtpunktzahl nicht 
> immer eindeutig ist, dieser Unterschied ändert jedoch nichts an den getroffenen Aussagen.

Für den Vergleich mit händisch erstellten "Optimalkorrekturen" als grundsätzliche Methode sehe 
ich keine Alternative, da die Menge der möglichen Fehler die eine studentische Lösung enthalten 
könnte nicht im Vorhinein absehbar ist. Es wird also nicht möglich sein, zuzusichern, dass ein 
automatisches Korrekturverfahren _alle Fehler_ findet, genauso wenig wie zugesichert werden 
kann, dass _alle korrekten Lösungen_ erkannt werden, wenn nicht im Vorhinein alle möglichen 
Lösungen bekannt sind und vom Instruktor bedacht werden. Der Maßstab zur Evaluation der 
automatischen Bewertung muss also relativ sein. Als Referenzwert können nur Bewertungen durch 
Tutoren dienen, weil Diese die _besten_ uns bekannten Bewertungen der vorliegenden Aufgabe sind.

> #### Note
> Nur weil ich mir keine andere grundsätzliche Methode vorstellen kann und in der Beschreibung
> der anderen Systeme keine Rede von absoluten Maßstäben für die Qualität von Bewertungen war,
> heißt das nicht, dass es keine gibt, auch wenn das nur logisch scheint. An dieser Stelle ist
> mehr Recherche notwendig.

Allerdings muss nicht zwangsläufig, wie bei [Bian] und [Striewe] erst die endgültige Note als
Referenzwert genutzt werden. Dieser Ansatz scheint der Einfachste, setzt er doch nur vorraus,
dass die automatische und die händische Bewertung auf dem gleichen Punkteschema (Im Sinne von
gleiche Punkte/Punktabzüge für den gleichen Fehler) basiert. Dazu kommt, dass nur wenig Arbeit
erbracht werden muss, bevor man in der Laage ist, die beiden Bewertungen zu vergleichen. 
Allerdings ignoriert der Ansatz viele mögliche Fehlerquellen, die im Kontext von INLOOM nicht 
ignoriert werden sollten, da es ja nicht lediglich um die Evaluation der Bewertung geht, sondern
auch darum, wie das Programm zu dieser Bewertung gekommen ist. Der Ansatz kann dazu dienen die
Frage: ``"Kann ich mich auf die Richtigkeit der Bewertung, die INLOOM vergibt, verlassen?"``
(__Frage 1__) oberflächlich zu beantworten.

Die endfültige Note/Gesamtpunktzahl, die auf eine studentische Lösung vergeben wird, ist ein sehr
grobgranularer Wert mit beschränkter Aussagekraft. Szenarien, in denen beide Korrekturverfahren
zwar die gleiche Gesamtpunktzahl vergeben, dies aber mit völlig verschiedenen Gründen tun, sind 
leicht vorstellbar.

> #### Note
> Cohens Kappa und AC1 scheinen solche Fälle zu berücksichtigen. 

Das kann, wenn es ausschließlich um die Bewertung studentischer Lösungen geht, eventuell 
akzeptiert werden, reicht aber für INLOOM nicht aus, da hier, abhängig vom genutzen Constraint 
und von der vergebenen Category Flag, automatisches Feedback für den Studenten generiert werden 
soll. Ein Szenario in dem nur zufällig die gleiche Bewertung vergeben wird ist daher 
inakzeptabel.

INLOOM nimmt dem Instruktor nicht nur die Aufgabe der Bewertung, sondern auch die Aufgabe ab 
Feedback zu geben. Der Instruktor stellt sich die Frage: ``"Kann ich mich darauf verlassen,
dass das Programm dem Studenten passendes Feedback gibt?"`` (__Frage 2__) Um diese Frage zu 
beantworten, muss sichergestellt werden, dass INLOOM nicht nur einen Fehler findet wo einer ist, 
sondern auch richtig erkennt _warum_ es sich um einen Fehler handelt. Es muss also das 
Constraint zum Finden des Fehlers genutzt werden, welches auch zum Finden dieses Fehlers gedacht 
ist. 

Dem Instruktor sollte vermittelt werden, an welcher Stelle noch ein oder mehrere Constraints 
fehlen. So könnte er, beim Erstellen neuer Constraints, wiederholt die Testsuite, auf die, durch 
die Constraints generierten Resultate, anwenden und Schritt für Schritt Fehlerquellen ausmerzen. 
``"An welcher Stelle müssen Constraints verbessert oder hinzugefügt werden, bevor ich die Arbeit 
von INLOOM verantworten kann?"`` (__Frage 3__).

> #### Question
> An der Beantwortung welcher anderen Fragen könnte der Instruktor noch interessiert sein?

## Possible Reference Attributes
Wenn ich mich nicht irre, dann setzt jede Evaluation der Bewertung, die nicht ausschließlich 
anhand der resultierenden Note durchgeführt wird voraus, dass ein "korrekter" Datensatz 
generiert wird, auf den die Tests angewendet werden können. Es müssen also Daten über die 
_korrekte Auswertung_ erfasst und persistiert werden.

Optimal wäre natürlich, wenn man eine Referenz Bewertung durch einen manuellen Korrekteur 
gänzlich als XML (siehe DTD) digitalisieren könnte. Eine komplette Digitalisierung bedeutet 
einen großen Overhead in der Erstellung von Testdatensätzen. Dieser Overhead sollte so stark wir 
möglich reduziert werden. Es ist denkbar zu diesem Zweck einen graphischen Editor zu 
implementieren, der die Eingabe von manuellen Bewertungen erleichtert. Einmal eingegeben, 
könnten die digitalisierte manuelle Korrektur (__manEval__) und die von INLOOM automatisch 
generierte Bewertung (__autoEval__), direkt mit einander verglichen werden.

Ein solcher Vergleich würde dann anhand einer Auswahl von XML Elements stattfinden: Den 
"Reference Attributes". Offensichtlich würde der Vergleich vornehmlich anhand der Inhalte von 
Results, also den einzelnen Result-s stattfinden, da jede Stufe darüber auf eine Evaluation 
anhand der Note hinauslaufen würde. Es wäre sinnvoll, die Eingabe der manEval auf die gewählten 
Reference Attributes zu reduzieren.

1. TestObject & RuleObject

    Anhand TestObjects & RuleObject kann überprüft werden, ob INLOOM für dieses Result das 
    korrekte Element gematched hat. Ich denke dieses Element zu checken ist immer sinnvoll, da 
    sich ja schon hier entscheidet, ob eine weitere Betrachtung sinnvoll ist.

2. RuleSet & Rule

    RuleSet und Rule identifizieren das zur Erzeugung des Result verwendete Constraint eindeutig.
    Diese Information ist relevant um Constraint _Überdeckung_ zu vermeiden. Das Hinzufügen eines
    neuen Constraints könnte dazu führen, dass ein Anderes nicht länger in den gewünschten 
    Fällen zur Anwendung kommt und dem Studenten dadurch falsches Feedback gegeben wird.

3. Category & Points

    Category und Points können verwendet werden um zu prüfen, dass nicht nur das richtige 
    Constraint zur Erzeugung des Results verwendet wurde, sondern aus der Anwendung des 
    Constraints auch die korrekte Punktebewertung resultiert.

__manEval__ und der von __autoEval__ können weiterhin anhand beliebiger statistischer Werte auf 
Basis der bisher aufgezählten Attribute verglichen werden. Ein simples Beispiel für einen 
solchen Wert, ist die Anzahl der der einzelnen Category Flags in beiden XML Dateien.

> #### Question
> Welche Attribute, sind am besten als Reference Attributes geeignet (geben also am besten 
> Antwort auf Frage 1 bis 3)? 

Aus den beiden Evals müsste eine Testdatenstruktur abgeleitet werden, von der ich mir vorstellen 
kann, dass sie etwa so aussehen könnte:

> #### Note
> Diese Datenstruktur ist direkt abhängig von der angegebenen DTD und muss nach dem Update der 
> DTD vermutlich angepasst werden.

``` python
# PYTHON PSEUDOCODE
# °°°°°°°°°°°°°°°°°

@dataclass
class TestDataSet:
    """This is a TestDataSet. It contains all the data
    necessary, to compare two evaluations of the same
    student model for test purposes."""

    rule_model: str # Id of the expert solution used for the evaluation
    test_model: str # Id of the student solution used for the evaluation
    possible_points: float # Maximum number of points possible
    autoEval: Evaluation # Automatically generated Evaluaion
    manEval: Evaluation # Manually produced Evaluation

@dataclass
class Evaluation: 
    """This is a represention of an evaluation created
    for a student model, by either a person, or the 
    automated system being tested."""

    results: Map[ResultKey, ResultData] # The (results in|constraints employed) by Eval.
    result_points: float # Points awarded by this Eval
    additionalData: Map[str, Any] # Any additional data (time_created, manual_tutor, ..)

@dataclass
class ResultKey:
    """This is a ResultKey. A result key contains all
    the information required to explicitly identify a
    result extracted from a result xml file."""

    test_object: str # Label of the test model object matched by the result
    rule_object: str # Label of the expert model object matched by the result
    rule_set: str # Id of the rule group employed by this result
    rule: str # Id of the rule employed by this result

    def __eq__(self, other):
        """This class would have to be comparable."""
        ...

@dataclass
class ResultData:
    """This is the ResultData. It basically contains 
    the 'primitive' data of a result."""

    category: Category # Category flag the constraint produced
    points: float # Number of points awarded by evaluation
    message: str # Feedback message the student received.

class Category(Enum):
    """Enum of the possible cateory Flags."""

    CORRECT = 0
    WARNING = 1
    ERROR = 2
    MISSING = 3
    INFO = 4


```

## Prozessintegration
> #### Note
> Ich habe derzeit nur eine oberflächliche Vorstellung vom Prozess (wie oben zu sehen). Um den 
> Nutzen der zu erstellenden Testsuite zu maximieren, sollte ich auf jeden Fall eine 
> eingehendere Prozessanalyse vornehmen.

Ich stelle mir, für die Prozessintegration der Testsuite, ein Vorgehen in zwei Schritten vor. Im 
ersten Schritt, möchte der Instruktor wissen, ob es notwendig ist Nachbesserungen an den 
derzeitigen Constraints vorzunehmen. Ich stelle mir diesen Schritt _Referenz generierend_ vor. 
Es wird immer einen Punkt geben, an dem man zur Einschätzung: "Good Enough" kommt - und nicht 
vorhat weitere Verbesserungen am System vorzunehmen. Eine gewisse Fehlertoleranz ist schon 
allein desshalb notwendig, weil die Evaluationen studentischer Lösungen nicht immer objektiv 
sein müssen. Zwar können durch "moderated marks" [Thomas] oder "clean scores" [Hamann 5.2.2] die 
Auswirkungen von Subjektivität minimiert werden, jedoch ist anzunehmen, dass sich manEval und 
autoEval immer zu einem gewissen, akzeptierbaren Grad unterscheiden werden.

Die Testsuite muss den Instruktor in die Laage versetzen, erkennen zu können, ob er "Good 
Enough" erreicht oder schon überschritten hat. Ich denke, dass eine solche Einschätzung, auf 
einem möglichst (breiten|großen|statistisch relevanten) Datensatz beruhen sollte. Das wiederum 
bedeutet, dass der Aufwand zur Erstellung eines solchen Datensatzes, zur Generierung einer 
Qualitäts Referenz, möglichst klein sein muss. Es könnte also sinnvoll sein, optimal Bewertungen 
(optimal Result-XML ?) auf zwei verschiedenen Detail Levels zu erstellen. 

Das _gröbere_ Detail Level würde ausschließlich Attribute enthalten, die mit wenig Aufwand in 
das Testset einpflegbar sind. Also Attribute, die aus händischen Lösungen abgeschrieben und 
beispielsweise via csv eingepflegt werden können. Anhand dieser Attribute könnten simple Tests 
durchgeführt werden, die dazu dienen einen groben Überblick, über die Bewertungsperformance von 
INLOOM zu gewinnen. Durch die reduzierte Dimension der eingegebenen Daten, wäre es möglich, 
schnell eine große Test Datenbasis aufzubauen, da es nicht notwendig wäre, die manEval 
vollständig digital zu reproduzieren. Die so gewonnen Daten könnten dazu ausreichen __Frage 1__ 
zu beantworten und Hinweise auf __Frage 3__ zu geben. 

Es könnten zum Beispiel Punkte pro Object (Test-/RuleObject) erfasst werden, oder die absolute 
Anzahl der gefundenen Correct/Warning/Error Flags (und ihrer händischen Entsprechung) in den 
beiden Lösungen. 

> #### Note
> [Thomas, Smith, Waugh] verwendet die von [Gwet] vorgeschlagene AC1 Statistic zur Bewertung von 
> "[Inter Rater Reliability]". Ich habe vor mich mit dieser zu beschäftigen. Alternative 
> Statistiken zu AC1 sind (ich entnehme das verschiedenen Erwähnungen) Cohen's Kappa, sowie 
> Fleiss's Kappa und Krippendorff's alpha. Außerdem ist häufig die Rede von "pi statistics" wie 
> zum Beispiel "[Scott's Pi]". 
> 
> Werte dieser Art werden genutzt um zu bewerten, wie sehr zwei Evaluationen, abhängig vom 
> Bewertenden, voneinander abweichen. Keiner der Werte scheint: _Algorithmisch schwierig zu 
> berechnen_ - zu sein. Ich sollte mich vermutlich mit einigen solcher Werte auseinander setzen 
> und eine Auswahl treffen. Es ist durchaus vorstellbar mehrere dieser Werte automatisch zu 
> berechnen, sollte sich herausstellen, dass sie eine interessante Indikation liefern.

## Bewertungs Wizard

Auf einer solchen Datenbasis wäre aber wohl kaum ein so detailierter Testfall vorstellbar, wie 
ihn die Beantwortung von __Frage 2__ erfordert. Für Solche, müssen die __manEval__ gänzlich 
formal digitalisiert werden. 

Die Digitalisierung dieser Daten bedeutet einen Aufwand, der _so stark wie möglich_ reduziert 
werden sollte. Ich schlage vor, zu diesem Zweck, sollte es so etwas noch nicht geben, eine Art 
"Bewertungswizard" zu bauen, mit dem Tutoren studentische Lösungen bewerten können. 

Die optimal Lösung wird side-by-side mit der studentischen Lösung angezeigt. Der Wizard 
leitet den Tutor durch die einzelnen Bewertungsschritte. Durch die Implementierung eines solchen 
"Wizards" würde sichergestellt, dass die Tutoren das gleiche Bewertungsschema verwenden wie 
INLOOM. 

Sie könnten während der normalen Korrektur dazu beitragen INLOOM zu verbessern, indem sie, wenn 
sie einen Fehler finden, den sie keinem bestehenden Constraint zuordnen können, eine "Missing 
Constraint" Meldung generieren. Der Constraint Ersteller würde über das Fehlen eines Constraints 
benachrichtigt werden. Nachdem das neue Constraint hinzugefügt wurde, kann der Tutor die 
Korrektur des Studenten Modells fortsetzen. 

Die verfügbaren Constraints könnten leicht über ein Git Repo aktuell gehalten werden. Es müsste 
nicht einmal der vollständige Constraint Code an alle Nutzer des Wizards verteilte werden. Ein 
Register der verfügbaren Constraints, zusammen mit einer Beschreibung, des durch das Constraint 
abgedeckten Fehlers, würde ausreichen. 

### Einsatz des Wizards in der Bewerungspraxis
Der Einsatz eines solchen Wizards in der tagtäglichen Bewertungs Praxis, würde nicht nur dazu 
beigetragen, die Qualität von INLOOM, durch einen "nebenbei" umfangreicher werdenden Test 
Datensatz, zu verbessern, sondern auch eine Formalisierung des Bewertungsprozesses bedeuten. Ein 
Formalisierter Bewertungsprozess bedeutet weniger Arbeitsaufwand für die Tutoren und sorgt für 
mehr Fairness in der Benotung der Studenten. Die zu benotende studentische Lösung müsste nicht 
einmal in formalisierter digitaler Form (etwa als Eclipse Output) zur Verfügung stehen. Ein Bild 
oder Scan der Lösung, würde für die Zwecke des Wizards genügen. Eine spätere digitale 
Reproduktion der studentischen Lösung im von INLOOM unterstützen Format, würde die Evaluation 
für den Testbetrieb verfügbar machen. Es könnte sogar versucht werden, die Struktur der 
studentischen Lösung aus der eingegebenen Evaluation abzuleiten. Der Fakt, dass eine solche 
Rekonstruktion möglich ist, würde beweisen, dass die Evaluation _alles_ bedacht hat. Ein 
Rekonstruktionsversuch, könnte dem Tutor die Bewertung vereinfachen, indem er ihn darauf 
hinweist, welches notwendige Kriterium er noch nicht bedacht hat.

Die resultierenden würden digital vorliegen und wären einfach zugänglich, für den Studenten, 
aber auch für Peer-Reviews durch andere Tutoren, oder einen der Lehrverantwortlichen.

### Bewertungsschritte
DerWizard müsste den Tutor durch folgende Bewertungsschritte führen:

1. Matching der Elemente

    Wizard listet alle Elemente der Expertenlösung auf. Der Tutor wird aufgefordert, für jedes 
    der gelisteten Elemente, das entsprechende Label in der studentischen Lösung anzugeben. Die 
    resultierenden Daten sollten in der Laage sein, einen Großteil der "arbitrary" Constraints 
    befriedigen zu können.

2. Auflistung der Fehler

    Der Tutor muss Gelegenheit bekommen, die Constraintbrüche, die er in der studentischen 
    Lösung findet, zu dokumentieren. Für jeden neu registrierten "Fehler" muss der Tutor das 
    gematchte Element und gebrochene Constraint wählen, sowie die Fehler Category des 
    Constraintbruchs. Es ist denkbar, dem Tutor die Möglichkeit zu geben einen Freitext 
    Kommentar einzugeben, der dazu genutzt werden kann Constraint Feedback Messages zu 
    optimieren.
    
    > #### ___Note___
    >"Wer morgen coole Sachen machen will, muss heute anfangen Daten ahnungsloser 
    > Nutzer zu sammeln." - Google 
    
    Alle nicht registrierten Constraits werden als Correct angenommen. Innerhalb des Wizards ist 
    ein "Report missing Constraint"-Feature denkbar, welches der Tutor nutzen kann um auf einen 
    Fehler hinzuweisen, welcher durch keines der verfügbaren Constraints abgedeckt wird. 

3. Zentrales Speichern der Vorgenommenen Evaluation

    In diesem Schritt spielt der Tutor nurnoch eine untergeordnete Rolle. Er "submitted" seine 
    Evaluation der studentischen Lösung. Ich könnte mir ein Git Repo vorstellen, in dem "Todo-" 
    und "Done-Evaluations" verwaltet werden. Eine Mögliche Reposturktur könnte so aussehen:
    
    ```
    Evaluation-Repo \
        |
        | Student-Group-{student_group_id} \
            |
            | Modelling-Exercise-{exercise_id} \
                |
                | expert-solution-{exercide_id}.png
                | Todo-Evaluations \
                    |
                    | solution-s-{student_id}-e-{exercide_id}.png
                    | ...
                | Done-Evaluations \
                    |
                    | Evaluation-S-{student_id}-E-{exercide_id} \
                        |
                        | solution-s-{student_id}-e-{exercide_id}.png
                        | evaluation-s-{student_id}-e-{exercide_id}-r-{rater_id}.json
                    | ...
                | ...
            | ...
        | ...
    ```

Dürch eine zentrale Verwaltung von Lösungen und Bewertungen, könnten zu korrigierende Aufgaben 
über Übungsgruppen hinweg auf Tutoren verteilt werden, wodurch negative Effekte unterschiedlich 
stark belegter Übungsgruppen nivelliert werden könnten, sollten die Übungsgruppen einen 
"Bewertungsaufwand" für den Tutor bedeuten. 

Außerdem wäre denkbar, dass studentische Lösungen, __anonymisiert__, für Peer Review durch 
Studenten anderer Übungsgruppen, zur Verfügung gestellt werden. Eine studentische Lösung, wird 
aus dem Todo- in den Donefolder verschoben, sobald mindestens eine Tutorenevaluation für sie 
vorliegt. Diese Optimalkorrektur kann nicht nur zu Testzwecken verwendet werden, sondern auch 
für Übungsaufgaben im studentischen Umfeld, wie: "Was hat dieser Student falsch gemacht?". Durch 
die Konfrontation des Studenten mit den Fehlern Anderer, kann er eventuell lernen die selben 
Fehler vermeiden. Eine Bewertung der studentischen Performance bei der Fehlersuche wäre über 
einen ähnlichen Prozess möglich, wie er auch bei der Bewertung von INLOOMS Fehlersuche zum 
Einsatz kommen soll.

> #### ___NOTE___
> LOTS OF FUN STUFF !!!11!elf

[//]: # (LINKS)
[Inter Rater Reliability]: https://de.wikipedia.org/wiki/Interrater-Reliabilit%C3%A4t
[Scott's Pi]: https://en.wikipedia.org/wiki/Scott%27s_Pi

[//]: # (IMAGES)