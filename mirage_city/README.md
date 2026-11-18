# Mirage City 🌴

Jeu d'action en monde ouvert (3D, navigateur) dans une métropole du désert inspirée de Dubaï.
Mode « bac à sable » : tout est débloqué, pas d'argent, pas d'étoiles de recherche, invincible.

## Lancer

Ouvre simplement `index.html` dans un navigateur récent (Chrome, Edge, Safari, Firefox).
Une connexion Internet est nécessaire au premier chargement (Three.js est chargé depuis un CDN).

## Contenu

1. **Créateur de personnage** : silhouette, taille, corpulence, teint, coiffure, barbe, couvre-chef
   (ghutra, foulard, casquette, chapeau), tenue (t-shirt, chemise, costume, sweat, débardeur, kandura, abaya),
   couleurs, accessoires. Sauvegardé dans le navigateur.
2. **La ville** : très haute tour centrale, hôtel en forme de voile sur son île (avec héliport),
   île en forme de palmier, marina et tours torsadées, mall à dôme, cadre doré géant, fontaine dansante,
   plage, désert avec dunes, autoroute et oasis. Cycle jour/nuit, météo (brume, tempête de sable), feux d'artifice.
3. **Quartier de Genève** (au nord) : vieille ville aux toits pentus avec commerces (boulangerie, horlogerie,
   chocolatier, fromagerie…), mairie avec horloge, cathédrale, hôpital (héliport sur le toit), police, caserne des
   pompiers, poste, gare routière, parkings, horloge fleurie, quai et lac avec jet d'eau et voiliers, Alpes à l'horizon.
4. **Campagne** : champs, vignobles, trois fermes (chalet, grange, silo), vaches et moutons, tracteurs.
5. **Mobilier urbain** : feux tricolores, trottoirs, bancs, poubelles, bornes à incendie, abribus, kiosques, fontaines.
6. **Vue cinéma** : vue à la première personne (V), graphismes cinéma (lueurs, grain, vignettage), nuits plus
   atmosphériques, vitrines éclairées, halos des lampadaires, trams et caténaires à Genève, passages piétons jaunes.
7. **Téléphone** (T) : GPS avec itinéraire par les routes, appels (taxi, police 117, pompiers 118, ambulance 144,
   mécano, pilote d'hélico), garage, météo, mode photo, réglages.
8. **Rendu réaliste** (3 niveaux : Standard, Cinéma, Ultra, ajustement automatique selon les performances) :
   textures PBR générées par le code (bitume, pavés, dalles, herbe, sable ridé, tuiles, façades avec vitres
   réfléchissantes), peinture automobile vernie, occlusion ambiante (GTAO), anticrénelage MSAA, ombres 4K,
   étalonnage des couleurs, netteté, flou de vitesse, reflets d'objectif, pluie avec chaussée mouillée et flaques.
9. **Personnages articulés** : squelette de 18 os (colonne, cou, tête, épaules, coudes, poignets, hanches,
   genoux, chevilles), corps aux formes arrondies, visage détaillé (yeux et iris, sourcils, nez, lèvres, oreilles,
   pommettes), choix de la couleur des yeux, zoom sur le visage dans le créateur. Animations procédurales :
   marche et course avec flexion des genoux et des coudes, respiration au repos, regard vers le joueur,
   passants au téléphone, mains en l'air quand on les vise, déséquilibre après un choc léger, moulinets en l'air,
   bras tendus avant l'impact, pose au sol propre à chacun et relèvement en deux temps.
10. **Tenues et accessoires réalistes** (joueur) : matériaux séparés pour la peau (reflet sous-cutané),
    les cheveux (reflet anisotrope), les tissus (trame, maille, denim), le cuir, le métal, le verre et les yeux.
    Chemise (col, boutons, poche, motifs uni / carreaux / rayures / fleurs), short avec ourlet, jean avec coutures,
    casquette (6 panneaux, visière, à l'endroit ou à l'envers), cagoule, gants noirs en cuir, montre (boîtier
    métal, verre, bracelet cuir), lunettes (montures dorées, verres réfléchissants), chaîne à maillons. Baskets,
    baskets montantes ou chaussures en cuir, avec couleur du dessus, de la semelle et de la bande latérale.
11. **Monuments reconnaissables** : Burj Khalifa (plan en Y, retraits en spirale), Burj Al Arab (exosquelette,
    héliport, restaurant suspendu), Palm Jumeirah et Atlantis, Dubai Mall, fontaine de Dubaï, Musée du Futur,
    Emirates Towers, Coca-Cola Arena, Dubai Frame, Dubai Marina ; à Genève : jet d'eau, vieille ville et
    cathédrale, Palais des Nations et chaise cassée, Stade de Genève, grands hôtels du quai, rue des horlogers.
12. **Frontière et aéroport** : mur et postes de douane avec barrières automatiques et drapeaux entre Dubaï et
    Genève ; aéroport international dans le désert (piste, terminal, tour de contrôle, hangars) et jet privé pilotable.
13. **Gameplay** : circulation et piétons, 17 véhicules (supercars, hypercar en or, 4x4, quad, moto, taxi,
   patrouille, limousine, bus, ambulance, camion de pompiers, fourgon postal, tracteur, hélicoptère, jet-ski, yacht), 5 armes (poings, pistolet, fusil, lance-roquettes,
   canon à confettis), jetpack, parachute, super saut, super vitesse, ralenti, téléportation par la carte.
14. **Intérieurs visitables** (F devant une porte dorée) : galerie du Dubai Mall (boutiques, fontaine, escalator,
    passants), hall du Grand Hôtel du Lac (colonnes, lustres, réception), horlogerie de luxe (essayer une montre en
    or, en acier ou noire) et hall des départs de l'aéroport (comptoirs, tableau des vols, sièges).
15. **Vie urbaine** : cycle des feux synchronisé (les voitures s'arrêtent au rouge, les piétons attendent pour
    traverser), bus qui marquent l'arrêt aux abribus, clignotants, feux stop et de recul, phares qui éclairent la
    route la nuit, habitacle visible en vue intérieure (tableau de bord, sièges, volant qui tourne).
16. **Garde-robe et garage** : jusqu'à 8 tenues enregistrées (créateur ou téléphone), peinture et néons sous caisse
    pour son véhicule, mémorisés pour les prochains appels au garage.
17. **Mode photo** (téléphone → Photo) : caméra libre, 6 filtres, profondeur de champ, focale, 6 poses, capture
    téléchargeable en JPEG.
18. **Ciel physique et végétation** : diffusion atmosphérique (Rayleigh/Mie), nuages animés selon la météo,
    palmiers et arbres détaillés qui ondulent au vent, herbe dans les parcs et la campagne.
19. **Animation** : clignement des yeux, mâchoire qui bouge au téléphone, doigts qui se referment sur l'arme.
20. **Performances et sauvegarde** : niveaux de détail (véhicules et piétons lointains simplifiés, herbe par zones),
    résolution dynamique pour viser 50–60 images/s, sauvegarde automatique toutes les 8 s et bouton « Continuer ».

## Commandes

| Touche | Action |
|---|---|
| ZQSD / WASD / flèches | Se déplacer / conduire |
| Souris | Caméra (cliquer pour la capturer) |
| Maj | Sprint / nitro |
| Espace | Saut, frein à main, monter (hélico/jetpack), parachute en chute |
| C / Ctrl | Descendre (hélico/jetpack) |
| F | Monter / descendre d'un véhicule, entrer / sortir d'un bâtiment, interagir |
| Clic | Tirer / frapper |
| 1-5, R | Changer d'arme |
| J | Jetpack |
| H | Klaxon / sirène |
| M | Carte : itinéraire GPS et téléportation |
| V | Vue à la première personne |
| T | Téléphone |
| G | Effacer l'itinéraire |
| Échap | Menu (garage, armes, téléport, monde, pouvoirs, personnage) |

Sur mobile : joystick à gauche, glisser à droite pour la caméra, boutons d'action.

## Déployer sur Streamlit Community Cloud

- Repository : ce dépôt, branche `main`
- Main file path : `mirage_city/streamlit_app.py`

Dans Streamlit, clique d'abord dans le jeu pour lui donner le focus clavier.
Si la capture de la souris est bloquée, maintiens le clic et glisse pour tourner la caméra.

## Développement

Le code est découpé en modules dans `src/` :

- `src/template.html` : styles et interface ;
- `src/js/NN-*.js` : modules JavaScript, concaténés dans l'ordre des numéros (portée partagée).

`index.html` est généré : après une modification dans `src/`, lance

```bash
python3 mirage_city/build.py
```

`python3 mirage_city/build.py --check` vérifie qu'`index.html` est à jour (utilisé par la CI).

Test de fumée (Chromium en rendu logiciel, nécessite Playwright) :

```bash
node mirage_city/tests/smoke.mjs
```
