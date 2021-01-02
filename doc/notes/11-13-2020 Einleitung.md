# INLOOM QT

## Meeting Notes
Im Meeting vom 13.11.2020 habe ich mit Hr. Hamann über die Ergebnisse meiner Recherche zum Thema 
IRR gesprochen. Da die Ergebnisse eher negativer Natur waren, sind wir an der Stelle aber nicht 
weit gekommen. Ich werde mir weiterhin Gedanken zu sinnvollen statistischen Werten machen, die 
eine Aussage über den Gesamtstatus des Systems zulassen. Sollte ich zu diesem Thema keine Idee 
zum weiteren Vorgehen in der Literatur finden können, ist es auch okay, wenn ich mir 
selbstständig etwas neues überlege. Wir haben außerdem meine nächsten Schritt besprochen. Ich 
soll, bis zu unserem nächsten Treffen am **04.12.2020** , einen Ablaufplan für die Arbeit 
ausarbeiten. Dabei soll ich darauf achten mir am Ende der Arbeit ausreichend Puffer für 
eventuelle Korrekturen zu lassen (Der Vorschlag waren etwa 2 Wochen). Es ist sinnvoll, den 
schriftlichen und praktischen Teil zeitlich parallel zu bearbeiten und Gedanken zu einem Thema 
direkt schriftlich festzuhalten. Außerdem soll ich bis zum nächsten Meeting einen ersten Entwurf 
für Einleitung und Literaturanalyse schreiben, den Hr. Hammann dann bis zu unserem nächsten 
Treffen reviewen kann. Die Zielangabe für diesen ersten Entwurf ist zu Researchquestions zu 
gelangen, die das Ziel der Arbeit formalisieren und im Evalutionsteil evaluiert werden können. 

## Manuelle Evaluationen
Seit dem letzten Meeting verfüge ich außerdem über die manuellen Korrekturen, die zu den mir 
bereits vorliegenden automatischen Korrekturen passen. Diese muss ich auf aus ihnen erfassbare 
Werte untersuchen. Dieser Schritt ist besonders wichtig, weil sich hier entscheidet, welche 
Vergleiche meine später zu implementierende Software vornehmen kann.

## Projektplan
| KW | Schriftteil | Praxisteil | Meeting |
| -- | ----------- | ---------- | ------- |
| 47 | Erstentwurf: Einleitung & Literaturanalyse. Zielsetzung: Research Questions. | Implementierung von grundlegender Infrasturktur (DBConnection, XMLAdapter, Dataclasses). | Nein |
| 48 | Erstentwurf: Einleitung & Literaturanalyse. Zielsetzung: Research Questions. | Implementierung von grundlegender Infrasturktur (DBConnection, XMLAdapter, Dataclasses). | Nein |
| 49 | Erstentwurf: Einleitung & Literaturanalyse. Zielsetzung: Research Questions. | Implementierung von grundlegender Infrasturktur (DBConnection, XMLAdapter, Dataclasses). | 04.12.2020 |
| 50 | Erstentwurf: Softwareentwurf | Implementierung Reference Data Input | Nein |
| 51 | Erstentwurf: Softwareentwurf | Implementierung Reference Data Input | Ja |
| 52 | Erstentwurf: Softwareentwurf | Implementierung TestEngine | Nein |
| 53 | Erstentwurf: Implementierung | Implementierung TestEngine | Ja |
| 01 | Erstentwurf: Implementierung | Implementierung Output Visualization | Nein |
| 02 | Finalisierung: Implementierung | Implementierung TestEngine | Ja |
| 03 | Erstentwurf: AutoEval | Finalisierung | Nein |
| 04 | Finalisierung: AutoEval, Review | Finalisierung | Ja |
| 05 | Review | Review | Nein |

## Erste Kapitel _Schreiben_


> ### **PAUL! WORTE! SCHREIBEN! JETZT!**


1. Einleitung

    1. Motivation
    2. Research Questions

        Neuen Bedarf an Digitalem Unterricht Decken

2. Related Work

    1. INLOOM

        |
        Kurze Einleitung zu INLOOM. Intention; Funktionsweise (i.S.v. Algorithmus, nichts technisches); Probleme;

    2. Quality Testing in existing ITS

        |
        Welche Konzepte zum Quality Testing verwenden literaturbekannte ITS.
        Wie habe ich meine Literaturrecherche durchgeführt

        2. Inter-Rater-Reliability

            |
            What is interrater reliability?

            1. Scott's Pi
            2. AC1 Statistic

    3. Supervised Learning
    
        Beim Supervised Learning erhält ein Algorithmus ein Set von gelabelten 
        Trainingsdaten. Gelabelt meint im Kontext von Machine Learing, dass zu einem Datensatz 
        das gewünschte Resultat gegeben ist. Bei gewöhnlichem Supervised Learning, erzeugt ein 
        *Algorithmus* aus diesen gelabelten Input Daten, durch einen Optimierungs- 
        beziehungsweise Lernprozess, eine Funktion, also ein Mapping von Input Vekotor zu Output 
        Vektor. Der Output Vektor ist solcher Form, dass er mit den gegebenen gewünschten 
        Resultaten verglichen werden kann. Durch den Vergleich des *eigenen* Resultats, zu einem 
        bestimmten Input Vektor, mit dem, bei diesem Vektor erwarteten Resultat, ist der 
        Algorithmus in der Lage seine Funktion inferierte Funktion anzupassen um das von ihr 
        produzierte Ergebnis dem erwarteten anzugleichen. 
        
        Bei INLOOM übernimmt diesen Schritt der Funktionserstellung der Instruktor. INLOOM setzt 
        also kein Supervised Learning ein, aber alle Eigenschaften der Input/Output Datensätze 
        von INLOOM stimmen mit denen eines Supervised Learning Algorithmus überein.

        Meine Aufgabe kann verstanden werden als: Finde ein Similarity Measure zwischen manEval 
        und autoEval.

3. INLOOM QT

    
