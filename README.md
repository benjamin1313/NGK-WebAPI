# NGK-WebAPI

## Formål:

At demonstrere opfyldelse af læringsmålet:
- Beskrive hvorledes man opbygger et Web Api som følger REST arkitekturen

## Det skal gruppen aflevere:

En journalen som indledes med en forside, hvor hver af gruppens medlemmer er anført med studienummer og navn.
Journalen skal indeholde en kort beskrivelse af udviklingsforløbet,
og dokumentere at serveren virker som krævet i opgaven.Et bilag til journalen som skal indeholde alt det udviklede kode i en zip-fil, samt en video som demonstrerer at jeres WebAPIopfylder kravene.

## Krav til anvend teknologi:
Du vælger selv, om du vil løse opgaven med C# og ASP.Net Core eller med Phyton og Flask.

## Opgavebeskrivelse:
Lav en web server som kører på en Raspberry Pi og som har funktionalitet til at tænde og slukke for en lampe/diode samt kan aflæse en værdi på Pi'en -f.eks. om en kontakt er on eller off.Endvidere skal serveren kunne udsende enalarm via WebSocket-protokollen ved tryk på en kontakt.

## Krav til webAPI:
Lav et webAPIhvormeden klient kan:
- Hente status på en kontakt (open eller closed).
- Tænde eller slukke for en lysdiode.

## Krav til webSocket forbindelse:
Det skal være muligt for klienter at tilmelde sig til at få alarm, når det trykkes på en kontakt forbundet til R.Pi. Dette skal implementeres ved brug af en WebSocket forbindelse -evt. ved brug af SignalR teknologi, hvis den valgte server understøtter dette.

## Krav til sikkerhed:
En klient skal være logget ind, for at kunne tænde eller slukke for en lysdiode. Serverens api skal derfor indeholde endpoints til oprette nye klienter, og mulighed for at eksisterende klienter kan logge ind. Serveren skal benytte JWT som authentificationstoken.

## Krav til testning:
At serveren opfylder de specificerede krav skal dokumenteres ved brug af programmet Postman. Og for studerende, som har eller har haft kurset Softwaretest gælder, at de også skal teste controllerklasserne med nogle udvalgte unittests.
