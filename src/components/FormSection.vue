<template>
  <section class="section bg">
    <div class="container">
      <div class="box border">
        <h1 class="title">
          Europe is still buying Russian oil. How much does Putin profit when we fly?
        </h1>
        <div class="calculate-form">
          <div class="form-group">
            <label for="iata1" class="form-label icon icon-plane"><icon-plane></icon-plane></label>
            <AutoComplete forceSelection v-model="iata1" :suggestions="filteredAirports1" @complete="searchAirport1($event)" field="airport" id="iata1" class="form-input" placeholder="from" @input="calculate()" />
          </div>
          <div class="checkbox-group">
            <input class="calculate-checkbox-input" checked type="checkbox" id="return" v-model="checked" @change="calculate($event)" />
            <label class="calculate-checkbox-label" for="return">
              <icon-return-way v-if="checked"></icon-return-way>
              <icon-single-way v-else></icon-single-way>
            </label>
          </div>
          <div class="form-group">
            <label for="iata2" class="form-label icon reverse icon-plane"><icon-plane></icon-plane></label>
            <AutoComplete forceSelection v-model="iata2" :suggestions="filteredAirports2" @complete="searchAirport2($event)" field="airport" id="iata2" class="form-input" placeholder="to" @input="calculate()" />
          </div>
        </div>
        <div v-if="moneytorussia != 0" class="result-wrapper">
          <div class="calculate-result">
            <span class="calculate-result-value">= {{ moneytorussia }}€ to Putin for oil</span>
          </div>
          <Transition>
            <div class="result-donate">
              <a class="btn bg-blue" href="https://donate.redcrossredcrescent.org/ua/donate/~my-donation">Donate</a>
              <span class="result-donate-msg">to the Red Cross Ukraine emergency appeal</span>
            </div>
          </Transition>
        </div>
      </div>
    </div>
    <modal-loading v-if="loading"></modal-loading>
  </section>
</template>

<script>
import AutoComplete from 'primevue/autocomplete';
import ModalLoading from '../components/ModalLoading.vue'
import IconPlane from './IconPlane.vue';
import IconReturnWay from './IconReturnWay.vue';
import IconSingleWay from './IconSingleWay.vue';
const API_URL = 'https://api.putinhuil.io/flight/'

export default {
  name: 'FormSection',
  components: { 
    AutoComplete,
    IconPlane,
    IconReturnWay,
    IconSingleWay,
    ModalLoading
  },
  data() {
    return {
      checked: true,
      filteredAirports1: null,
      filteredAirports2: null,
      iata1: null,
      iata2: null,
      jsn: null,
      moneytorussia: 0,
      returnflight: 1,
      loading: false,
      items: [
      {airport: "Tirana International Airport Mother Teresa", iata: "TIA"}, {airport: "Graz Airport", iata: "GRZ"}, {airport: "Innsbruck Airport", iata: "INN"}, {airport: "Linz Hörsching Airport", iata: "LNZ"}, {airport: "Salzburg Airport", iata: "SZG"}, {airport: "Vienna International Airport", iata: "VIE"}, {airport: "Klagenfurt Airport", iata: "KLU"}, {airport: "Hohenems-Dornbirn Airport", iata: "HOH"}, {airport: "Antwerp International Airport (Deurne)", iata: "ANR"}, {airport: "Brussels Airport", iata: "BRU"}, {airport: "Brussels South Charleroi Airport", iata: "CRL"}, {airport: "Wevelgem Airport", iata: "KJK"}, {airport: "Liège Airport", iata: "LGG"}, {airport: "Ostend-Bruges International Airport", iata: "OST"}, {airport: "Zoersel (Oostmalle) Airfield", iata: "OBL"}, {airport: "Mostar International Airport", iata: "OMO"}, {airport: "Sarajevo International Airport", iata: "SJJ"}, {airport: "Banja Luka International Airport", iata: "BNX"}, {airport: "Tuzla International Airport", iata: "TZL"}, {airport: "Burgas Airport", iata: "BOJ"}, {airport: "Gorna Oryahovitsa Airport", iata: "GOZ"}, {airport: "Plovdiv International Airport", iata: "PDV"}, {airport: "Sofia Airport", iata: "SOF"}, {airport: "Stara Zagora Airport", iata: "SZR"}, {airport: "Varna Airport", iata: "VAR"}, {airport: "Bezmer Air Base", iata: "JAM"}, {airport: "Larnaca International Airport", iata: "LCA"}, {airport: "Paphos International Airport", iata: "PFO"}, {airport: "RAF Akrotiri", iata: "AKT"}, {airport: "Ercan International Airport", iata: "ECN"}, {airport: "Lefkoniko Airport", iata: "GEC"}, {airport: "Aarhus Airport", iata: "AAR"}, {airport: "Billund Airport", iata: "BLL"}, {airport: "Copenhagen Kastrup Airport", iata: "CPH"}, {airport: "Esbjerg Airport", iata: "EBJ"}, {airport: "Karup Airport", iata: "KRP"}, {airport: "Læsø Airport", iata: "BYR"}, {airport: "Lolland Falster Maribo Airport", iata: "MRW"}, {airport: "Odense Airport", iata: "ODE"}, {airport: "Copenhagen Roskilde Airport", iata: "RKE"}, {airport: "Bornholm Airport", iata: "RNN"}, {airport: "Sønderborg Airport", iata: "SGD"}, {airport: "Skrydstrup Air Base", iata: "SKS"}, {airport: "Skive Airport", iata: "SQW"}, {airport: "Thisted Airport", iata: "TED"}, {airport: "Stauning Airport", iata: "STA"}, {airport: "Aalborg Airport", iata: "AAL"}, {airport: "Sindal Airport", iata: "CNL"}, {airport: "Cork Airport", iata: "ORK"}, {airport: "Galway Airport", iata: "GWY"}, {airport: "Dublin Airport", iata: "DUB"}, {airport: "Ireland West Knock Airport", iata: "NOC"}, {airport: "Kerry Airport", iata: "KIR"}, {airport: "Shannon Airport", iata: "SNN"}, {airport: "Sligo Airport", iata: "SXL"}, {airport: "Waterford Airport", iata: "WAT"}, {airport: "Donegal Airport", iata: "CFN"}, {airport: "Inishmore Aerodrome", iata: "IOR"}, {airport: "Connemara Regional Airport", iata: "NNR"}, {airport: "Inisheer Aerodrome", iata: "INQ"}, {airport: "Inishmaan Aerodrome", iata: "IIA"}, {airport: "Bantry Aerodrome", iata: "BYT"}, {airport: "Kärdla Airport", iata: "KDL"}, {airport: "Kuressaare Airport", iata: "URE"}, {airport: "Pärnu Airport", iata: "EPU"}, {airport: "Lennart Meri Tallinn Airport", iata: "TLL"}, {airport: "Tartu Airport", iata: "TAY"}, {airport: "Kunovice Airport", iata: "UHE"}, {airport: "Karlovy Vary International Airport", iata: "KLV"}, {airport: "Ostrava Leos Janáček Airport", iata: "OSR"}, {airport: "Pardubice Airport", iata: "PED"}, {airport: "Přerov Air Base", iata: "PRV"}, {airport: "Václav Havel Airport Prague", iata: "PRG"}, {airport: "Brno-Tuřany Airport", iata: "BRQ"}, {airport: "Vodochody Airport", iata: "VOD"}, {airport: "Enontekio Airport", iata: "ENF"}, {airport: "Halli Airport", iata: "KEV"}, {airport: "Helsinki Malmi Airport", iata: "HEM"}, {airport: "Helsinki Vantaa Airport", iata: "HEL"}, {airport: "Hyvinkää Airfield", iata: "HYV"}, {airport: "Kitee Airport", iata: "KTQ"}, {airport: "Ivalo Airport", iata: "IVL"}, {airport: "Joensuu Airport", iata: "JOE"}, {airport: "Jyvaskyla Airport", iata: "JYV"}, {airport: "Kauhava Airport", iata: "KAU"}, {airport: "Kemi-Tornio Airport", iata: "KEM"}, {airport: "Kajaani Airport", iata: "KAJ"}, {airport: "Kauhajoki Airport", iata: "KHJ"}, {airport: "Kokkola-Pietarsaari Airport", iata: "KOK"}, {airport: "Kuusamo Airport", iata: "KAO"}, {airport: "Kittilä Airport", iata: "KTT"}, {airport: "Kuopio Airport", iata: "KUO"}, {airport: "Lahti Vesivehmaa Airport", iata: "QLF"}, {airport: "Lappeenranta Airport", iata: "LPP"}, {airport: "Mariehamn Airport", iata: "MHQ"}, {airport: "Mikkeli Airport", iata: "MIK"}, {airport: "Oulu Airport", iata: "OUL"}, {airport: "Pori Airport", iata: "POR"}, {airport: "Rovaniemi Airport", iata: "RVN"}, {airport: "Savonlinna Airport", iata: "SVL"}, {airport: "Sodankyla Airport", iata: "SOT"}, {airport: "Tampere-Pirkkala Airport", iata: "TMP"}, {airport: "Turku Airport", iata: "TKU"}, {airport: "Utti Air Base", iata: "UTI"}, {airport: "Vaasa Airport", iata: "VAA"}, {airport: "Varkaus Airport", iata: "VRK"}, {airport: "Ylivieska Airfield", iata: "YLI"}, {airport: "Seinäjoki Airport", iata: "SJY"}, {airport: "Calais-Dunkerque Airport", iata: "CQF"}, {airport: "Albert-Bray Airport", iata: "BYF"}, {airport: "Le Touquet-Côte d'Opale Airport", iata: "LTQ"}, {airport: "Valenciennes-Denain Airport", iata: "XVS"}, {airport: "Agen-La Garenne Airport", iata: "AGF"}, {airport: "Bordeaux-Mérignac Airport", iata: "BOD"}, {airport: "Bergerac-Roumanière Airport", iata: "EGC"}, {airport: "Cognac-Châteaubernard (BA 709) Air Base", iata: "CNG"}, {airport: "Poitiers-Biard Airport", iata: "PIS"}, {airport: "Montluçon-Guéret Airport", iata: "MCU"}, {airport: "Limoges Airport", iata: "LIG"}, {airport: "Niort-Souché Airport", iata: "NIT"}, {airport: "Toulouse-Blagnac Airport", iata: "TLS"}, {airport: "Pau Pyrénées Airport", iata: "PUF"}, {airport: "Tarbes-Lourdes-Pyrénées Airport", iata: "LDE"}, {airport: "Angoulême-Brie-Champniers Airport", iata: "ANG"}, {airport: "Brive Souillac Airport", iata: "BVE"}, {airport: "Périgueux-Bassillac Airport", iata: "PGX"}, {airport: "Biarritz-Anglet-Bayonne Airport", iata: "BIQ"}, {airport: "Cahors-Lalbenque Airport", iata: "ZAO"}, {airport: "Albi-Le Séquestre Airport", iata: "LBI"}, {airport: "Castres-Mazamet Airport", iata: "DCM"}, {airport: "Rodez-Marcillac Airport", iata: "RDZ"}, {airport: "Royan-Médis Airport", iata: "RYN"}, {airport: "Montauban Airport", iata: "XMW"}, {airport: "Rochefort-Saint-Agnant (BA 721) Airport", iata: "RCO"}, {airport: "Colmar-Houssen Airport", iata: "CMR"}, {airport: "Dole-Tavaux Airport", iata: "DLE"}, {airport: "Aubenas-Ardèche Méridional Airport", iata: "OBS"}, {airport: "Le Puy-Loudes Airport", iata: "LPY"}, {airport: "Metz-Nancy-Lorraine Airport", iata: "ETZ"}, {airport: "Bastia-Poretta Airport", iata: "BIA"}, {airport: "Calvi-Sainte-Catherine Airport", iata: "CLY"}, {airport: "Figari Sud-Corse Airport", iata: "FSC"}, {airport: "Ajaccio-Napoléon Bonaparte Airport", iata: "AJA"}, {airport: "Propriano Airport", iata: "PRP"}, {airport: "Solenzara (BA 126) Air Base", iata: "SOZ"}, {airport: "Auxerre-Branches Airport", iata: "AUF"}, {airport: "Chambéry-Savoie Airport", iata: "CMF"}, {airport: "Clermont-Ferrand Auvergne Airport", iata: "CFE"}, {airport: "Bourges Airport", iata: "BOU"}, {airport: "Annemasse Airport", iata: "QNJ"}, {airport: "Lyon Saint-Exupéry Airport", iata: "LYS"}, {airport: "Saint-Yan Airport", iata: "SYT"}, {airport: "Roanne-Renaison Airport", iata: "RNE"}, {airport: "Annecy-Haute-Savoie-Mont Blanc Airport", iata: "NCY"}, {airport: "Grenoble-Isère Airport", iata: "GNB"}, {airport: "Valence-Chabeuil Airport", iata: "VAF"}, {airport: "Vichy-Charmeil Airport", iata: "VHY"}, {airport: "Aurillac Airport", iata: "AUR"}, {airport: "Châteauroux-Déols \"Marcel Dassault\" Airport", iata: "CHR"}, {airport: "Lyon-Bron Airport", iata: "LYN"}, {airport: "Cannes-Mandelieu Airport", iata: "CEQ"}, {airport: "Saint-Étienne-Bouthéon Airport", iata: "EBU"}, {airport: "Carcassonne Airport", iata: "CCF"}, {airport: "Marseille Provence Airport", iata: "MRS"}, {airport: "Nice-Côte d'Azur Airport", iata: "NCE"}, {airport: "Orange-Caritat (BA 115) Air Base", iata: "XOG"}, {airport: "Perpignan-Rivesaltes (Llabanère) Airport", iata: "PGF"}, {airport: "Le Castellet Airport", iata: "CTT"}, {airport: "Montpellier-Méditerranée Airport", iata: "MPL"}, {airport: "Béziers-Vias Airport", iata: "BZR"}, {airport: "Avignon-Caumont Airport", iata: "AVN"}, {airport: "Mende-Brenoux Airfield", iata: "MEN"}, {airport: "Paris Beauvais Tillé Airport", iata: "BVA"}, {airport: "Évreux-Fauville (BA 105) Air Base", iata: "EVX"}, {airport: "Le Havre Octeville Airport", iata: "LEH"}, {airport: "Abbeville", iata: "XAB"}, {airport: "Orléans-Bricy (BA 123) Air Base", iata: "ORE"}, {airport: "Châlons-Vatry Airport", iata: "XCR"}, {airport: "Rouen Airport", iata: "URO"}, {airport: "Tours-Val-de-Loire Airport", iata: "TUF"}, {airport: "Cholet Le Pontreau Airport", iata: "CET"}, {airport: "Laval-Entrammes Airport", iata: "LVA"}, {airport: "Paris-Le Bourget Airport", iata: "LBG"}, {airport: "Creil Air Base", iata: "CSF"}, {airport: "Charles de Gaulle International Airport", iata: "CDG"}, {airport: "Toussus-le-Noble Airport", iata: "TNF"}, {airport: "Paris-Orly Airport", iata: "ORY"}, {airport: "Pontoise - Cormeilles-en-Vexin Airport", iata: "POX"}, {airport: "Villacoublay-Vélizy (BA 107) Air Base", iata: "VIY"}, {airport: "Nevers-Fourchambault Airport", iata: "NVS"}, {airport: "Maubeuge-Élesmes Airport", iata: "XME"}, {airport: "Lille-Lesquin Airport", iata: "LIL"}, {airport: "Merville-Calonne Airport", iata: "HZB"}, {airport: "Charleville-Mézières Airport", iata: "XCZ"}, {airport: "Brest Bretagne Airport", iata: "BES"}, {airport: "Cherbourg-Maupertus Airport", iata: "CER"}, {airport: "Dinard-Pleurtuit-Saint-Malo Airport", iata: "DNR"}, {airport: "La Baule-Escoublac Airport", iata: "LBY"}, {airport: "Granville Airport", iata: "GFR"}, {airport: "Deauville-Saint-Gatien Airport", iata: "DOL"}, {airport: "Lorient South Brittany (Bretagne Sud) Airport", iata: "LRT"}, {airport: "La Roche-sur-Yon Airport", iata: "EDM"}, {airport: "Landivisiau Air Base", iata: "LDV"}, {airport: "Caen-Carpiquet Airport", iata: "CFR"}, {airport: "Le Mans-Arnage Airport", iata: "LME"}, {airport: "Rennes-Saint-Jacques Airport", iata: "RNS"}, {airport: "Lannion-Côte de Granit Airport", iata: "LAI"}, {airport: "Quimper-Cornouaille Airport", iata: "UIP"}, {airport: "Nantes Atlantique Airport", iata: "NTE"}, {airport: "Saint-Brieuc-Armor Airport", iata: "SBK"}, {airport: "Morlaix-Ploujean Airport", iata: "MXN"}, {airport: "Vannes-Meucon Airport", iata: "VNE"}, {airport: "Saint-Nazaire-Montoir Airport", iata: "SNR"}, {airport: "EuroAirport Basel-Mulhouse-Freiburg Airport", iata: "BSL"}, {airport: "Dijon-Bourgogne Airport", iata: "DIJ"}, {airport: "Metz-Frescaty (BA 128) Air Base", iata: "MZM"}, {airport: "Épinal-Mirecourt Airport", iata: "EPL"}, {airport: "Nancy-Essey Airport", iata: "ENC"}, {airport: "Reims-Champagne (BA 112) Air Base", iata: "RHE"}, {airport: "Strasbourg Airport", iata: "SXB"}, {airport: "Toulon-Hyères Airport", iata: "TLN"}, {airport: "Nîmes-Arles-Camargue Airport", iata: "FNI"}, {airport: "Île d'Yeu Airport", iata: "IDY"}, {airport: "Angers-Loire Airport", iata: "ANE"}, {airport: "La Môle Airport", iata: "LTT"}, {airport: "Gustaf III Airport", iata: "SBH"}, {airport: "Courchevel Airport", iata: "CVF"}, {airport: "La Rochelle-Île de Ré Airport", iata: "LRH"}, {airport: "Fréjus Airport", iata: "FRJ"}, {airport: "Megève Airport", iata: "MVV"}, {airport: "Méribel Altiport", iata: "MFX"}, {airport: "Fontaine Airport", iata: "BOR"}, {airport: "Gibraltar Airport", iata: "GIB"}, {airport: "Alderney Airport", iata: "ACI"}, {airport: "Guernsey Airport", iata: "GCI"}, {airport: "Narsarsuaq Airport", iata: "UAK"}, {airport: "Godthaab / Nuuk Airport", iata: "GOH"}, {airport: "Kangerlussuaq Airport", iata: "SFJ"}, {airport: "Thule Air Base", iata: "THU"}, {airport: "Ilulissat Airport", iata: "JAV"}, {airport: "Qasigiannguit Heliport", iata: "JCH"}, {airport: "Aasiaat Airport", iata: "JEG"}, {airport: "Alluitsup Paa Heliport", iata: "LLU"}, {airport: "Neerlerit Inaat Airport", iata: "CNP"}, {airport: "Paamiut Heliport", iata: "JFR"}, {airport: "Qeqertarsuaq Heliport", iata: "JGO"}, {airport: "Qaqortoq Heliport", iata: "JJU"}, {airport: "Maniitsoq Airport", iata: "JSU"}, {airport: "Nanortalik Heliport", iata: "JNN"}, {airport: "Narsaq Heliport", iata: "JNS"}, {airport: "Qaanaaq Airport", iata: "NAQ"}, {airport: "Sisimiut Airport", iata: "JHS"}, {airport: "Upernavik Airport", iata: "JUV"}, {airport: "Qaarsut Airport", iata: "JQA"}, {airport: "Ittoqqortoormiit Heliport", iata: "OBY"}, {airport: "Uummannaq Heliport", iata: "UMD"}, {airport: "Attu Heliport", iata: "QGQ"}, {airport: "Kangaatsiaq Heliport", iata: "QPW"}, {airport: "Kitsissuarsuit Heliport", iata: "QJE"}, {airport: "Ilimanaq Heliport", iata: "XIQ"}, {airport: "Qeqertaq Heliport", iata: "QQT"}, {airport: "Ikamiut Heliport", iata: "QJI"}, {airport: "Eqalugaarsuit Heliport", iata: "QFG"}, {airport: "Ikerassaarsuk Heliport", iata: "QRY"}, {airport: "Altenburg-Nobitz Airport", iata: "AOC"}, {airport: "Riesa-Göhlis Airport", iata: "IES"}, {airport: "Rechlin-Lärz Airport", iata: "REB"}, {airport: "Schönhagen Airport", iata: "QXH"}, {airport: "Barth Airport", iata: "BBH"}, {airport: "Magdeburg \"City\" Airport", iata: "ZMG"}, {airport: "Cottbus-Drewitz Airport", iata: "CBU"}, {airport: "Berlin-Schönefeld Airport", iata: "SXF"}, {airport: "Dresden Airport", iata: "DRS"}, {airport: "Erfurt Airport", iata: "ERF"}, {airport: "Frankfurt am Main Airport", iata: "FRA"}, {airport: "Münster Osnabrück Airport", iata: "FMO"}, {airport: "Hamburg Airport", iata: "HAM"}, {airport: "Berlin-Tempelhof International Airport", iata: "THF"}, {airport: "Cologne Bonn Airport", iata: "CGN"}, {airport: "Düsseldorf Airport", iata: "DUS"}, {airport: "Munich Airport", iata: "MUC"}, {airport: "Nuremberg Airport", iata: "NUE"}, {airport: "Leipzig/Halle Airport", iata: "LEJ"}, {airport: "Saarbrücken Airport", iata: "SCN"}, {airport: "Stuttgart Airport", iata: "STR"}, {airport: "Berlin-Tegel Airport", iata: "TXL"}, {airport: "Hannover Airport", iata: "HAJ"}, {airport: "Bremen Airport", iata: "BRE"}, {airport: "Frankfurt-Egelsbach Airport", iata: "QEF"}, {airport: "Frankfurt-Hahn Airport", iata: "HHN"}, {airport: "Mannheim-City Airport", iata: "MHG"}, {airport: "Eisenach-Kindel Airport", iata: "EIB"}, {airport: "Siegerland Airport", iata: "SGE"}, {airport: "Hamburg-Finkenwerder Airport", iata: "XFW"}, {airport: "Kiel-Holtenau Airport", iata: "KEL"}, {airport: "Lübeck Blankensee Airport", iata: "LBC"}, {airport: "Essen Mulheim Airport", iata: "ESS"}, {airport: "Bielefeld Airport", iata: "BFE"}, {airport: "Mönchengladbach Airport", iata: "MGL"}, {airport: "Paderborn Lippstadt Airport", iata: "PAD"}, {airport: "Dortmund Airport", iata: "DTM"}, {airport: "Augsburg Airport", iata: "AGB"}, {airport: "Oberpfaffenhofen Airport", iata: "OBF"}, {airport: "Straubing Airport", iata: "RBM"}, {airport: "Friedrichshafen Airport", iata: "FDH"}, {airport: "Schwerin Parchim Airport", iata: "SZW"}, {airport: "Bayreuth Airport", iata: "BYU"}, {airport: "Burg Feuerstein Airport", iata: "URD"}, {airport: "Hof-Plauen Airport", iata: "HOQ"}, {airport: "Zweibrücken Airport", iata: "ZQW"}, {airport: "Donaueschingen-Villingen Airport", iata: "ZQL"}, {airport: "Braunschweig-Wolfsburg Airport", iata: "BWE"}, {airport: "Kassel-Calden Airport", iata: "KSF"}, {airport: "Bremerhaven Airport", iata: "BRV"}, {airport: "Emden Airport", iata: "EME"}, {airport: "Wilhelmshaven-Mariensiel Airport", iata: "WVN"}, {airport: "Borkum Airport", iata: "BMK"}, {airport: "Norderney Airport", iata: "NRD"}, {airport: "Flensburg-Schäferhaus Airport", iata: "FLF"}, {airport: "Westerland Sylt Airport", iata: "GWT"}, {airport: "Spangdahlem Air Base", iata: "SPM"}, {airport: "Ramstein Air Base", iata: "RMS"}, {airport: "[Duplicate] Giebelstadt Army Air Field", iata: "GHF"}, {airport: "Celle Airport", iata: "ZCN"}, {airport: "Fritzlar Airport", iata: "FRZ"}, {airport: "Hanau Army Air Field", iata: "ZNF"}, {airport: "Flugplatz Kitzingen", iata: "KZG"}, {airport: "Nordholz Naval Airbase", iata: "FCN"}, {airport: "Geilenkirchen Air Base", iata: "GKE"}, {airport: "Rostock-Laage Airport", iata: "RLG"}, {airport: "Schleswig Air Base", iata: "WBG"}, {airport: "Wiesbaden Army Airfield", iata: "WIE"}, {airport: "Fürstenfeldbruck Air Base", iata: "FEL"}, {airport: "Ingolstadt Manching Airport", iata: "IGS"}, {airport: "Gütersloh Air Base", iata: "GUT"}, {airport: "Memmingen Allgau Airport", iata: "FMM"}, {airport: "Aachen-Merzbrück Airport", iata: "AAH"}, {airport: "Karlsruhe Baden-Baden Airport", iata: "FKB"}, {airport: "Weeze Airport", iata: "NRN"}, {airport: "Norden-Norddeich Airport", iata: "NOD"}, {airport: "Juist Airport", iata: "JUI"}, {airport: "Heringsdorf Airport", iata: "HDF"}, {airport: "Heide-Büsum Airport", iata: "HEI"}, {airport: "Helgoland-Düne Airport", iata: "HGL"}, {airport: "Rügen Airport", iata: "GTI"}, {airport: "Wangerooge Airport", iata: "AGE"}, {airport: "Langeoog Airport", iata: "LGO"}, {airport: "Emporia Municipal Airport", iata: "EMP"}, {airport: "Hunt Field", iata: "LND"}, {airport: "Lahr Airport", iata: "LHA"}, {airport: "Cochstedt Airport", iata: "CSO"}, {airport: "Köthen Airport", iata: "KOQ"}, {airport: "St. Peter-Ording Airport", iata: "PSH"}, {airport: "Peenemünde Airport", iata: "PEF"}, {airport: "Bitburg Airport", iata: "BBJ"}, {airport: "Neumünster Airport", iata: "EUM"}, {airport: "Neubrandenburg Airport", iata: "FNB"}, {airport: "Baltrum Airport", iata: "BMR"}, {airport: "Bonn-Hangelar Airport", iata: "BNJ"}, {airport: "Andravida Air Base", iata: "PYR"}, {airport: "Agrinion Air Base", iata: "AGQ"}, {airport: "Dimokritos Airport", iata: "AXD"}, {airport: "Nea Anchialos Airport", iata: "VOL"}, {airport: "Chios Island National Airport", iata: "JKH"}, {airport: "Ioannina Airport", iata: "IOA"}, {airport: "Heraklion International Nikos Kazantzakis Airport", iata: "HER"}, {airport: "Kastoria National Airport", iata: "KSO"}, {airport: "Kithira Airport", iata: "KIT"}, {airport: "Kefallinia Airport", iata: "EFL"}, {airport: "Kalamata Airport", iata: "KLX"}, {airport: "Kos Airport", iata: "KGS"}, {airport: "Karpathos Airport", iata: "AOK"}, {airport: "Ioannis Kapodistrias International Airport", iata: "CFU"}, {airport: "Kasos Airport", iata: "KSJ"}, {airport: "Alexander the Great International Airport", iata: "KVA"}, {airport: "Filippos Airport", iata: "KZI"}, {airport: "Leros Airport", iata: "LRS"}, {airport: "Limnos Airport", iata: "LXS"}, {airport: "Larisa Airport", iata: "LRA"}, {airport: "Mikonos Airport", iata: "JMK"}, {airport: "Mytilene International Airport", iata: "MJT"}, {airport: "Aktion National Airport", iata: "PVK"}, {airport: "Diagoras Airport", iata: "RHO"}, {airport: "Araxos Airport", iata: "GPA"}, {airport: "Chania International Airport", iata: "CHQ"}, {airport: "Skiathos Island National Airport", iata: "JSI"}, {airport: "Samos Airport", iata: "SMI"}, {airport: "Sparti Airport", iata: "SPJ"}, {airport: "Santorini Airport", iata: "JTR"}, {airport: "Sitia Airport", iata: "JSH"}, {airport: "Skiros Airport", iata: "SKU"}, {airport: "Thessaloniki Macedonia International Airport", iata: "SKG"}, {airport: "Zakynthos International Airport \"Dionysios Solomos\"", iata: "ZTH"}, {airport: "Eleftherios Venizelos International Airport", iata: "ATH"}, {airport: "Athen Helenikon Airport", iata: "HEW"}, {airport: "Astypalaia Airport", iata: "JTY"}, {airport: "Ikaria Airport", iata: "JIK"}, {airport: "Kalymnos Airport", iata: "JKL"}, {airport: "Milos Airport", iata: "MLO"}, {airport: "Naxos Airport", iata: "JNX"}, {airport: "Paros National Airport", iata: "PAS"}, {airport: "Kastelorizo Airport", iata: "KZS"}, {airport: "Syros Airport", iata: "JSY"}, {airport: "Porto Cheli Airport", iata: "PKH"}, {airport: "Dubrovnik Airport", iata: "DBV"}, {airport: "Osijek Airport", iata: "OSI"}, {airport: "Pula Airport", iata: "PUY"}, {airport: "Rijeka Airport", iata: "RJK"}, {airport: "Split Airport", iata: "SPU"}, {airport: "Zagreb Airport", iata: "ZAG"}, {airport: "Zadar Airport", iata: "ZAD"}, {airport: "Bol Airport", iata: "BWK"}, {airport: "Lošinj Island Airport", iata: "LSZ"}, {airport: "Budapest Liszt Ferenc International Airport", iata: "BUD"}, {airport: "Debrecen International Airport", iata: "DEB"}, {airport: "Pécs-Pogány Airport", iata: "PEV"}, {airport: "Sármellék International Airport", iata: "SOB"}, {airport: "Akureyri Airport", iata: "AEY"}, {airport: "Egilsstaðir Airport", iata: "EGS"}, {airport: "Hornafjörður Airport", iata: "HFN"}, {airport: "Húsavík Airport", iata: "HZK"}, {airport: "Ísafjörður Airport", iata: "IFJ"}, {airport: "Keflavik International Airport", iata: "KEF"}, {airport: "Patreksfjörður Airport", iata: "PFJ"}, {airport: "Reykjavik Airport", iata: "RKV"}, {airport: "Siglufjörður Airport", iata: "SIJ"}, {airport: "Vestmannaeyjar Airport", iata: "VEY"}, {airport: "Grímsey Airport", iata: "GRY"}, {airport: "Thorshofn Airport", iata: "THO"}, {airport: "Vopnafjörður Airport", iata: "VPN"}, {airport: "Reykjahlíð Airport", iata: "MVA"}, {airport: "Bildudalur Airport", iata: "BIU"}, {airport: "Gjögur Airport", iata: "GJR"}, {airport: "Sauðárkrókur Airport", iata: "SAK"}, {airport: "Norðfjörður Airport", iata: "NOR"}, {airport: "Grundarfjörður Airport", iata: "GUU"}, {airport: "Isle of Man Airport", iata: "IOM"}, {airport: "Crotone Airport", iata: "CRV"}, {airport: "Bari Karol Wojtyła Airport", iata: "BRI"}, {airport: "Foggia \"Gino Lisa\" Airport", iata: "FOG"}, {airport: "Taranto-Grottaglie \"Marcello Arlotta\" Airport", iata: "TAR"}, {airport: "Lecce Galatina Air Base", iata: "LCC"}, {airport: "Pescara International Airport", iata: "PSR"}, {airport: "Brindisi – Salento Airport", iata: "BDS"}, {airport: "Lamezia Terme Airport", iata: "SUF"}, {airport: "Catania-Fontanarossa Airport", iata: "CTA"}, {airport: "Lampedusa Airport", iata: "LMP"}, {airport: "Pantelleria Airport", iata: "PNL"}, {airport: "Falcone–Borsellino Airport", iata: "PMO"}, {airport: "Reggio Calabria Airport", iata: "REG"}, {airport: "Vincenzo Florio Airport Trapani-Birgi", iata: "TPS"}, {airport: "Sigonella Navy Air Base", iata: "NSY"}, {airport: "Alghero-Fertilia Airport", iata: "AHO"}, {airport: "Decimomannu Air Base", iata: "DCI"}, {airport: "Cagliari Elmas Airport", iata: "CAG"}, {airport: "Olbia Costa Smeralda Airport", iata: "OLB"}, {airport: "Tortolì Airport", iata: "TTB"}, {airport: "Malpensa International Airport", iata: "MXP"}, {airport: "Il Caravaggio International Airport", iata: "BGY"}, {airport: "Turin Airport", iata: "TRN"}, {airport: "Villanova D'Albenga International Airport", iata: "ALL"}, {airport: "Genoa Cristoforo Colombo Airport", iata: "GOA"}, {airport: "Milano Linate Airport", iata: "LIN"}, {airport: "Parma Airport", iata: "PMF"}, {airport: "Cuneo International Airport", iata: "CUF"}, {airport: "Aviano Air Base", iata: "AVB"}, {airport: "Bolzano Airport", iata: "BZO"}, {airport: "Bologna Guglielmo Marconi Airport", iata: "BLQ"}, {airport: "Treviso-Sant'Angelo Airport", iata: "TSF"}, {airport: "Forlì Airport", iata: "FRL"}, {airport: "Brescia Airport", iata: "VBS"}, {airport: "Trieste–Friuli Venezia Giulia Airport", iata: "TRS"}, {airport: "Federico Fellini International Airport", iata: "RMI"}, {airport: "Vicenza Airport", iata: "VIC"}, {airport: "Padova Airport", iata: "QPA"}, {airport: "Verona Villafranca Airport", iata: "VRN"}, {airport: "Venice Marco Polo Airport", iata: "VCE"}, {airport: "Siena-Ampugnano Airport", iata: "SAY"}, {airport: "Ciampino–G. B. Pastine International Airport", iata: "CIA"}, {airport: "Leonardo da Vinci–Fiumicino Airport", iata: "FCO"}, {airport: "Marina Di Campo Airport", iata: "EBA"}, {airport: "Latina Air Base", iata: "QLT"}, {airport: "Naples International Airport", iata: "NAP"}, {airport: "Pisa International Airport", iata: "PSA"}, {airport: "Peretola Airport", iata: "FLR"}, {airport: "Grosseto Air Base", iata: "GRS"}, {airport: "Perugia San Francesco d'Assisi – Umbria International Airport", iata: "PEG"}, {airport: "Ancona Falconara Airport", iata: "AOI"}, {airport: "Aosta Airport", iata: "AOT"}, {airport: "Salerno Costa d'Amalfi Airport", iata: "QSR"}, {airport: "Oristano-Fenosu Airport", iata: "FNU"}, {airport: "Comiso Airport", iata: "CIY"}, {airport: "Sarzana-Luni Air Base", iata: "QLP"}, {airport: "Jersey Airport", iata: "JER"}, {airport: "Liepāja International Airport", iata: "LPX"}, {airport: "Riga International Airport", iata: "RIX"}, {airport: "Ventspils International Airport", iata: "VNT"}, {airport: "Daugavpils Intrenational Airport", iata: "DGP"}, {airport: "Šiauliai International Airport", iata: "SQQ"}, {airport: "Barysiai Airport", iata: "HLJ"}, {airport: "Kaunas International Airport", iata: "KUN"}, {airport: "Palanga International Airport", iata: "PLQ"}, {airport: "Vilnius International Airport", iata: "VNO"}, {airport: "Panevėžys Air Base", iata: "PNV"}, {airport: "Klaipėda Airport", iata: "KLJ"}, {airport: "M. R. Štefánik Airport", iata: "BTS"}, {airport: "Košice Airport", iata: "KSC"}, {airport: "Piešťany Airport", iata: "PZY"}, {airport: "Sliač Airport", iata: "SLD"}, {airport: "Poprad-Tatry Airport", iata: "TAT"}, {airport: "Žilina Airport", iata: "ILZ"}, {airport: "Luxembourg-Findel International Airport", iata: "LUX"}, {airport: "Bălți International Airport", iata: "BZY"}, {airport: "Chişinău International Airport", iata: "KIV"}, {airport: "Podgorica Airport", iata: "TGD"}, {airport: "Tivat Airport", iata: "TIV"}, {airport: "Ohrid St. Paul the Apostle Airport", iata: "OHD"}, {airport: "Skopje Alexander the Great Airport", iata: "SKP"}, {airport: "Malta International Airport", iata: "MLA"}, {airport: "Xewkija Heliport", iata: "GZM"}, {airport: "Amsterdam Airport Schiphol", iata: "AMS"}, {airport: "Maastricht Aachen Airport", iata: "MST"}, {airport: "Eindhoven Airport", iata: "EIN"}, {airport: "Eelde Airport", iata: "GRQ"}, {airport: "Gilze Rijen Air Base", iata: "GLZ"}, {airport: "De Kooy Airport", iata: "DHR"}, {airport: "Lelystad Airport", iata: "LEY"}, {airport: "Leeuwarden Air Base", iata: "LWR"}, {airport: "Rotterdam The Hague Airport", iata: "RTM"}, {airport: "Soesterberg Air Base", iata: "UTC"}, {airport: "Twente Airport", iata: "ENS"}, {airport: "Valkenburg Naval Air Base", iata: "LID"}, {airport: "Woensdrecht Air Base", iata: "WOE"}, {airport: "Ålesund Airport", iata: "AES"}, {airport: "Andøya Airport", iata: "ANX"}, {airport: "Alta Airport", iata: "ALF"}, {airport: "Brønnøysund Airport", iata: "BNN"}, {airport: "Bodø Airport", iata: "BOO"}, {airport: "Bergen Airport Flesland", iata: "BGO"}, {airport: "Båtsfjord Airport", iata: "BJF"}, {airport: "Kristiansand Airport", iata: "KRS"}, {airport: "Geilo Airport Dagali", iata: "DLD"}, {airport: "Bardufoss Airport", iata: "BDU"}, {airport: "Harstad/Narvik Airport Evenes", iata: "EVE"}, {airport: "Leirin Airport", iata: "VDB"}, {airport: "Florø Airport", iata: "FRO"}, {airport: "Oslo Lufthavn", iata: "OSL"}, {airport: "Haugesund Airport", iata: "HAU"}, {airport: "Hasvik Airport", iata: "HAA"}, {airport: "Kristiansund Airport (Kvernberget)", iata: "KSU"}, {airport: "Kirkenes Airport (Høybuktmoen)", iata: "KKN"}, {airport: "Lista Airport", iata: "FAN"}, {airport: "Molde Airport", iata: "MOL"}, {airport: "Mosjøen Airport (Kjærstad)", iata: "MJF"}, {airport: "Banak Airport", iata: "LKL"}, {airport: "Notodden Airport", iata: "NTB"}, {airport: "Ørland Airport", iata: "OLA"}, {airport: "Røros Airport", iata: "RRS"}, {airport: "Moss Airport Rygge", iata: "RYG"}, {airport: "Svalbard Airport Longyear", iata: "LYR"}, {airport: "Skien Airport", iata: "SKE"}, {airport: "Stord Airport", iata: "SRP"}, {airport: "Sandnessjøen Airport (Stokka)", iata: "SSJ"}, {airport: "Tromsø Airport", iata: "TOS"}, {airport: "Sandefjord Airport Torp", iata: "TRF"}, {airport: "Trondheim Airport Værnes", iata: "TRD"}, {airport: "Stavanger Airport Sola", iata: "SVG"}, {airport: "Stokmarknes Skagen Airport", iata: "SKN"}, {airport: "Hammerfest Airport", iata: "HFT"}, {airport: "Valan Airport", iata: "HVG"}, {airport: "Mehamn Airport", iata: "MEH"}, {airport: "Vadsø Airport", iata: "VDS"}, {airport: "Ørsta-Volda Airport Hovden", iata: "HOV"}, {airport: "Narvik Framnes Airport", iata: "NVK"}, {airport: "Berlevåg Airport", iata: "BVG"}, {airport: "Oslo Fornebu Airport", iata: "FBU"}, {airport: "Leknes Airport", iata: "LKN"}, {airport: "Namsos Høknesøra Airport", iata: "OSY"}, {airport: "Mo i Rana Airport Røssvoll", iata: "MQN"}, {airport: "Rørvik Airport Ryum", iata: "RVK"}, {airport: "Røst Airport", iata: "RET"}, {airport: "Sandane Airport (Anda)", iata: "SDN"}, {airport: "Sogndal Airport", iata: "SOG"}, {airport: "Svolvær Helle Airport", iata: "SVJ"}, {airport: "Sørkjosen Airport", iata: "SOJ"}, {airport: "Vardø Airport Svartnes", iata: "VAW"}, {airport: "Værøy Heliport", iata: "VRY"}, {airport: "Stafsberg Airport", iata: "HMR"}, {airport: "Kautokeino Air Base", iata: "QKX"}, {airport: "Gdańsk Lech Wałęsa Airport", iata: "GDN"}, {airport: "Kraków John Paul II International Airport", iata: "KRK"}, {airport: "Katowice International Airport", iata: "KTW"}, {airport: "Poznań-Ławica Airport", iata: "POZ"}, {airport: "Rzeszów-Jasionka Airport", iata: "RZE"}, {airport: "Szczecin-Goleniów \"Solidarność\" Airport", iata: "SZZ"}, {airport: "Redzikowo Air Base", iata: "OSP"}, {airport: "Warsaw Chopin Airport", iata: "WAW"}, {airport: "Copernicus Wrocław Airport", iata: "WRO"}, {airport: "Zielona Góra-Babimost Airport", iata: "IEG"}, {airport: "Bydgoszcz Ignacy Jan Paderewski Airport", iata: "BZG"}, {airport: "Łódź Władysław Reymont Airport", iata: "LCJ"}, {airport: "Oksywie Military Air Base", iata: "QYD"}, {airport: "Radom Airport", iata: "RDO"}, {airport: "Modlin Airport", iata: "WMI"}, {airport: "Lublin Airport", iata: "LUZ"}, {airport: "Olsztyn-Mazury Airport", iata: "SZY"}, {airport: "Biała Podlaska Airfield", iata: "BXP"}, {airport: "Alverca Air Base", iata: "AVR"}, {airport: "Santa Maria Airport", iata: "SMA"}, {airport: "Bragança Airport", iata: "BGC"}, {airport: "Beja Airport / Airbase", iata: "BYJ"}, {airport: "Braga Municipal Aerodrome", iata: "BGZ"}, {airport: "Cascais Airport", iata: "CAT"}, {airport: "Flores Airport", iata: "FLW"}, {airport: "Faro Airport", iata: "FAO"}, {airport: "Graciosa Airport", iata: "GRW"}, {airport: "Horta Airport", iata: "HOR"}, {airport: "Lajes Airport", iata: "TER"}, {airport: "Monte Real Air Base", iata: "QLR"}, {airport: "João Paulo II Airport", iata: "PDL"}, {airport: "Pico Airport", iata: "PIX"}, {airport: "Portimão Airport", iata: "PRM"}, {airport: "Francisco de Sá Carneiro Airport", iata: "OPO"}, {airport: "Porto Santo Airport", iata: "PXO"}, {airport: "Humberto Delgado Airport (Lisbon Portela Airport)", iata: "LIS"}, {airport: "São Jorge Airport", iata: "SJZ"}, {airport: "Vila Real Airport", iata: "VRL"}, {airport: "Aerodromo Goncalves Lobato (Viseu Airport)", iata: "VSE"}, {airport: "Madeira Airport", iata: "FNC"}, {airport: "Corvo Airport", iata: "CVU"}, {airport: "Belgrade Nikola Tesla Airport", iata: "BEG"}, {airport: "Nis Airport", iata: "INI"}, {airport: "Priština International Airport", iata: "PRN"}, {airport: "Batajnica Air Base", iata: "BJY"}, {airport: "Cenej Airport", iata: "QND"}, {airport: "Arad International Airport", iata: "ARW"}, {airport: "Bacău Airport", iata: "BCM"}, {airport: "Tautii Magheraus Airport", iata: "BAY"}, {airport: "Băneasa International Airport", iata: "BBU"}, {airport: "Mihail Kogălniceanu International Airport", iata: "CND"}, {airport: "Cluj-Napoca International Airport", iata: "CLJ"}, {airport: "Caransebeş Airport", iata: "CSB"}, {airport: "Craiova Airport", iata: "CRA"}, {airport: "Iaşi Airport", iata: "IAS"}, {airport: "Oradea International Airport", iata: "OMR"}, {airport: "Henri Coandă International Airport", iata: "OTP"}, {airport: "Sibiu International Airport", iata: "SBZ"}, {airport: "Satu Mare Airport", iata: "SUJ"}, {airport: "Suceava Stefan cel Mare Airport", iata: "SCV"}, {airport: "Tulcea Airport", iata: "TCE"}, {airport: "Transilvania Târgu Mureş International Airport", iata: "TGM"}, {airport: "Timişoara Traian Vuia Airport", iata: "TSR"}, {airport: "Ljubljana Jože Pučnik Airport", iata: "LJU"}, {airport: "Maribor Airport", iata: "MBX"}, {airport: "Portoroz Airport", iata: "POW"}, {airport: "Fuerteventura Airport", iata: "FUE"}, {airport: "Hierro Airport", iata: "VDE"}, {airport: "La Palma Airport", iata: "SPC"}, {airport: "Gran Canaria Airport", iata: "LPA"}, {airport: "Lanzarote Airport", iata: "ACE"}, {airport: "Tenerife South Airport", iata: "TFS"}, {airport: "Tenerife Norte Airport", iata: "TFN"}, {airport: "Melilla Airport", iata: "MLN"}, {airport: "Albacete-Los Llanos Airport", iata: "ABC"}, {airport: "Alicante International Airport", iata: "ALC"}, {airport: "Almería International Airport", iata: "LEI"}, {airport: "Asturias Airport", iata: "OVD"}, {airport: "Córdoba Airport", iata: "ODB"}, {airport: "Bilbao Airport", iata: "BIO"}, {airport: "Barcelona International Airport", iata: "BCN"}, {airport: "Badajoz Airport", iata: "BJZ"}, {airport: "A Coruña Airport", iata: "LCG"}, {airport: "Girona Airport", iata: "GRO"}, {airport: "Federico Garcia Lorca Airport", iata: "GRX"}, {airport: "Ibiza Airport", iata: "IBZ"}, {airport: "Jerez Airport", iata: "XRY"}, {airport: "San Javier Airport", iata: "MJV"}, {airport: "Adolfo Suárez Madrid–Barajas Airport", iata: "MAD"}, {airport: "Málaga Airport", iata: "AGP"}, {airport: "Menorca Airport", iata: "MAH"}, {airport: "Moron Air Base", iata: "OZP"}, {airport: "Pamplona Airport", iata: "PNA"}, {airport: "Reus Air Base", iata: "REU"}, {airport: "Rota Naval Station Airport", iata: "ROZ"}, {airport: "Salamanca Airport", iata: "SLM"}, {airport: "San Sebastian Airport", iata: "EAS"}, {airport: "Santiago de Compostela Airport", iata: "SCQ"}, {airport: "Pirineus - la Seu d'Urgel Airport", iata: "LEU"}, {airport: "Torrejón Airport", iata: "TOJ"}, {airport: "Valencia Airport", iata: "VLC"}, {airport: "Valladolid Airport", iata: "VLL"}, {airport: "Vitoria/Foronda Airport", iata: "VIT"}, {airport: "Vigo Airport", iata: "VGO"}, {airport: "Santander Airport", iata: "SDR"}, {airport: "Zaragoza Air Base", iata: "ZAZ"}, {airport: "Sevilla Airport", iata: "SVQ"}, {airport: "Palma De Mallorca Airport", iata: "PMI"}, {airport: "La Gomera Airport", iata: "GMZ"}, {airport: "Logroño-Agoncillo Airport", iata: "RJL"}, {airport: "Leon Airport", iata: "LEN"}, {airport: "Burgos Airport", iata: "RGS"}, {airport: "Sabadell Airport", iata: "QSA"}, {airport: "Lleida-Alguaire Airport", iata: "ILD"}, {airport: "Huesca/Pirineos Airport", iata: "HSK"}, {airport: "Ciudad Real Central Airport", iata: "CQM"}, {airport: "Cuatro Vientos Airport", iata: "ECV"}, {airport: "Castellón-Costa Azahar Airport", iata: "CDT"}, {airport: "Teruel Airport", iata: "TEV"}, {airport: "Algeciras Heliport", iata: "AEI"}, {airport: "Región de Murcia International Airport", iata: "RMU"}, {airport: "Ronneby Airport", iata: "RNB"}, {airport: "Gothenburg-Landvetter Airport", iata: "GOT"}, {airport: "Jönköping Airport", iata: "JKG"}, {airport: "Lidköping-Hovby Airport", iata: "LDK"}, {airport: "Gothenburg City Airport", iata: "GSE"}, {airport: "Skövde Airport", iata: "KVB"}, {airport: "Trollhättan-Vänersborg Airport", iata: "THN"}, {airport: "Karlskoga Airport", iata: "KSK"}, {airport: "Mora Airport", iata: "MXX"}, {airport: "Stockholm Skavsta Airport", iata: "NYO"}, {airport: "Kristianstad Airport", iata: "KID"}, {airport: "Oskarshamn Airport", iata: "OSK"}, {airport: "Kalmar Airport", iata: "KLR"}, {airport: "Malmö Sturup Airport", iata: "MMX"}, {airport: "Halmstad Airport", iata: "HAD"}, {airport: "Växjö Kronoberg Airport", iata: "VXO"}, {airport: "Sveg Airport", iata: "EVG"}, {airport: "Gällivare Airport", iata: "GEV"}, {airport: "Hudiksvall Airport", iata: "HUV"}, {airport: "Kramfors Sollefteå Airport", iata: "KRF"}, {airport: "Lycksele Airport", iata: "LYC"}, {airport: "Sundsvall-Härnösand Airport", iata: "SDL"}, {airport: "Örnsköldsvik Airport", iata: "OER"}, {airport: "Kiruna Airport", iata: "KRN"}, {airport: "Skellefteå Airport", iata: "SFT"}, {airport: "Umeå Airport", iata: "UME"}, {airport: "Vilhelmina Airport", iata: "VHM"}, {airport: "Arvidsjaur Airport", iata: "AJR"}, {airport: "Örebro Airport", iata: "ORB"}, {airport: "Stockholm Västerås Airport", iata: "VST"}, {airport: "Luleå Airport", iata: "LLA"}, {airport: "Stockholm-Arlanda Airport", iata: "ARN"}, {airport: "Stockholm-Bromma Airport", iata: "BMA"}, {airport: "Borlange Airport", iata: "BLE"}, {airport: "Hultsfred Airport", iata: "HLF"}, {airport: "Gävle Sandviken Airport", iata: "GVX"}, {airport: "Linköping City Airport", iata: "LPI"}, {airport: "Norrköping Airport", iata: "NRK"}, {airport: "Eskilstuna Airport", iata: "EKT"}, {airport: "Visby Airport", iata: "VBY"}, {airport: "Åre Östersund Airport", iata: "OSD"}, {airport: "Hagfors Airport", iata: "HFS"}, {airport: "Karlstad Airport", iata: "KSD"}, {airport: "Torsby Airport", iata: "TYF"}, {airport: "Ängelholm-Helsingborg Airport", iata: "AGH"}, {airport: "Storuman Airport", iata: "SQO"}, {airport: "Hemavan Airport", iata: "HMV"}, {airport: "Pajala Airport", iata: "PJA"}, {airport: "Söderhamn Airport", iata: "SOO"}, {airport: "Geneva Cointrin International Airport", iata: "GVA"}, {airport: "Sion Airport", iata: "SIR"}, {airport: "Emmen Air Base", iata: "EML"}, {airport: "Lugano Airport", iata: "LUG"}, {airport: "Bern Belp Airport", iata: "BRN"}, {airport: "Grenchen Airport", iata: "ZHI"}, {airport: "Zürich Airport", iata: "ZRH"}, {airport: "St Gallen Altenrhein Airport", iata: "ACH"}, {airport: "Samedan Airport", iata: "SMV"}, {airport: "Lausanne-Blécherette Airport", iata: "QLS"}, {airport: "Locarno Airport", iata: "ZJI"}, {airport: "Neuchatel Airport", iata: "QNC"}, {airport: "Interlaken Air Base", iata: "ZIN"}, {airport: "Buochs Airport", iata: "BXO"}, {airport: "Belfast International Airport", iata: "BFS"}, {airport: "St Angelo Airport", iata: "ENK"}, {airport: "George Best Belfast City Airport", iata: "BHD"}, {airport: "City of Derry Airport", iata: "LDY"}, {airport: "Birmingham International Airport", iata: "BHX"}, {airport: "Coventry Airport", iata: "CVT"}, {airport: "Gloucestershire Airport", iata: "GLO"}, {airport: "Cotswold Airport", iata: "GBA"}, {airport: "Manchester Airport", iata: "MAN"}, {airport: "Newquay Cornwall Airport", iata: "NQY"}, {airport: "RAF Lyneham", iata: "LYE"}, {airport: "RNAS Yeovilton", iata: "YEO"}, {airport: "Haverfordwest Airport", iata: "HAW"}, {airport: "Cardiff International Airport", iata: "CWL"}, {airport: "Swansea Airport", iata: "SWS"}, {airport: "Bristol Airport", iata: "BRS"}, {airport: "Liverpool John Lennon Airport", iata: "LPL"}, {airport: "London Luton Airport", iata: "LTN"}, {airport: "Plymouth City Airport", iata: "PLH"}, {airport: "Bournemouth Airport", iata: "BOH"}, {airport: "Southampton Airport", iata: "SOU"}, {airport: "Lasham Airport", iata: "QLA"}, {airport: "Shoreham Airport", iata: "ESH"}, {airport: "London Biggin Hill Airport", iata: "BQH"}, {airport: "London Gatwick Airport", iata: "LGW"}, {airport: "London City Airport", iata: "LCY"}, {airport: "Farnborough Airport", iata: "FAB"}, {airport: "Blackbushe Airport", iata: "BBS"}, {airport: "London Heathrow Airport", iata: "LHR"}, {airport: "Southend Airport", iata: "SEN"}, {airport: "Lydd Airport", iata: "LYX"}, {airport: "Kent International Airport", iata: "MSE"}, {airport: "Carlisle Airport", iata: "CAX"}, {airport: "Blackpool International Airport", iata: "BLK"}, {airport: "Humberside Airport", iata: "HUY"}, {airport: "Barrow Walney Island Airport", iata: "BWF"}, {airport: "Leeds Bradford Airport", iata: "LBA"}, {airport: "Warton Airport", iata: "WRT"}, {airport: "Hawarden Airport", iata: "CEG"}, {airport: "Newcastle Airport", iata: "NCL"}, {airport: "Durham Tees Valley Airport", iata: "MME"}, {airport: "East Midlands Airport", iata: "EMA"}, {airport: "Kirkwall Airport", iata: "KOI"}, {airport: "Sumburgh Airport", iata: "LSI"}, {airport: "Wick Airport", iata: "WIC"}, {airport: "Aberdeen Dyce Airport", iata: "ABZ"}, {airport: "Inverness Airport", iata: "INV"}, {airport: "Glasgow International Airport", iata: "GLA"}, {airport: "Edinburgh Airport", iata: "EDI"}, {airport: "Islay Airport", iata: "ILY"}, {airport: "Glasgow Prestwick Airport", iata: "PIK"}, {airport: "Benbecula Airport", iata: "BEB"}, {airport: "Scatsta Airport", iata: "SCS"}, {airport: "Dundee Airport", iata: "DND"}, {airport: "Stornoway Airport", iata: "SYY"}, {airport: "Tiree Airport", iata: "TRE"}, {airport: "RAF Leuchars", iata: "ADX"}, {airport: "RAF Lossiemouth", iata: "LMO"}, {airport: "Cambridge Airport", iata: "CBG"}, {airport: "Norwich International Airport", iata: "NWI"}, {airport: "London Stansted Airport", iata: "STN"}, {airport: "Exeter International Airport", iata: "EXT"}, {airport: "Bristol Filton Airport", iata: "FZO"}, {airport: "Oxford (Kidlington) Airport", iata: "OXF"}, {airport: "RAF Benson", iata: "BEX"}, {airport: "RAF Lakenheath", iata: "LKZ"}, {airport: "RAF Mildenhall", iata: "MHZ"}, {airport: "RAF Wyton", iata: "QUY"}, {airport: "RAF Fairford", iata: "FFD"}, {airport: "RAF Brize Norton", iata: "BZZ"}, {airport: "RAF Odiham", iata: "ODH"}, {airport: "RAF Northolt", iata: "NHT"}, {airport: "RAF Coningsby", iata: "QCY"}, {airport: "RAF Honington", iata: "BEQ"}, {airport: "RAF Scampton", iata: "SQZ"}, {airport: "RAF Linton-On-Ouse", iata: "HRT"}, {airport: "RAF Waddington", iata: "WTN"}, {airport: "RAF Marham", iata: "KNF"}, {airport: "St. Mary's Airport", iata: "ISC"}, {airport: "Nottingham Airport", iata: "NQT"}, {airport: "Campbeltown Airport", iata: "CAL"}, {airport: "Eday Airport", iata: "EOI"}, {airport: "Fair Isle Airport", iata: "FIE"}, {airport: "North Ronaldsay Airport", iata: "NRL"}, {airport: "Papa Westray Airport", iata: "PPW"}, {airport: "Stronsay Airport", iata: "SOY"}, {airport: "Sanday Airport", iata: "NDY"}, {airport: "Lerwick / Tingwall Airport", iata: "LWK"}, {airport: "Westray Airport", iata: "WRY"}, {airport: "Land's End Airport", iata: "LEQ"}, {airport: "Penzance Heliport", iata: "PZE"}, {airport: "Anglesey Airport", iata: "VLY"}, {airport: "Barra Airport", iata: "BRR"}, {airport: "Outer Skerries Airport", iata: "OUK"}, {airport: "Unst Airport", iata: "UNT"}, {airport: "Oban Airport", iata: "OBN"}, {airport: "Lympne Airport", iata: "LYM"}, {airport: "Colonsay Airstrip", iata: "CSA"}, {airport: "Wycombe Air Park", iata: "HYC"}, {airport: "Bembridge Airport", iata: "BBP"}, {airport: "Perth/Scone Airport", iata: "PSL"}, {airport: "Duxford Aerodrome", iata: "QFO"}, {airport: "Rochester Airport", iata: "RCS"}, {airport: "Redhill Aerodrome", iata: "KRH"}, {airport: "Chichester/Goodwood Airport", iata: "QUG"}, {airport: "RAF Kinloss", iata: "FSS"}, {airport: "St. Helena Airport", iata: "HLE"}, {airport: "Boryspil International Airport", iata: "KBP"}, {airport: "Donetsk International Airport", iata: "DOK"}, {airport: "Dnipropetrovsk International Airport", iata: "DNK"}, {airport: "Simferopol International Airport", iata: "SIP"}, {airport: "Kiev Zhuliany International Airport", iata: "IEV"}, {airport: "Lviv International Airport", iata: "LWO"}, {airport: "Odessa International Airport", iata: "ODS"}, {airport: "Mariupol International Airport", iata: "MPW"}, {airport: "Luhansk International Airport", iata: "VSG"}, {airport: "Zaporizhzhia International Airport", iata: "OZH"}, {airport: "Kryvyi Rih International Airport", iata: "KWG"}, {airport: "Kharkiv International Airport", iata: "HRK"}, {airport: "Ivano-Frankivsk International Airport", iata: "IFO"}, {airport: "Chernivtsi International Airport", iata: "CWC"}, {airport: "Rivne International Airport", iata: "RWN"}, {airport: "Uzhhorod International Airport", iata: "UDJ"}, {airport: "Lutsk Airport", iata: "UCK"}, {airport: "Chernihiv Shestovitsa Airport", iata: "CEJ"}, {airport: "Cherkasy International Airport", iata: "CKC"}, {airport: "Mykolaiv International Airport", iata: "NLV"}, {airport: "Kherson International Airport", iata: "KHE"}, {airport: "Kirovograd Airport", iata: "KGO"}, {airport: "Belbek Airport", iata: "UKS"}, {airport: "Kerch Airport", iata: "KHC"}, {airport: "Gostomel Airport", iata: "GML"}, {airport: "Vinnytsia/Gavyryshivka Airport", iata: "VIN"}, {airport: "Suprunovka Airport", iata: "PLV"}, {airport: "Khmelnytskyi Airport", iata: "HMJ"}, {airport: "Zhytomyr Airport", iata: "ZTR"}, {airport: "Kramatorsk Airport", iata: "KRQ"}, {airport: "Berdyansk Airport", iata: "ERD"}
      ]
    }
  },
  watch: {
    iata1: {
      handler(newValue) {
        console.log(newValue);
        this.calculate();
      }, deep: true
    },
    iata2: {
      handler(newValue) {
        console.log(newValue);
        this.calculate();
      }, deep: true
    }
  },
  methods: {
    async calculate() {
      try {
        if (this.iata1.iata && this.iata2.iata) {
          this.loading = true;
          const url = API_URL + '?iata1=' + this.iata1.iata + '&iata2=' + this.iata2.iata + '&ret=' + this.checked;
          this.jsn = await (await fetch(url)).json();
          this.moneytorussia = this.jsn.message;
          this.loading = false;
        }
      }
      catch (TypeError)	{
        console.log('');
      }
    },
    searchAirport1(event) {
      this.filteredAirports1 = this.searchAirports(event.query);
    },
    searchAirport2(event) {
      this.filteredAirports2 = this.searchAirports(event.query);
    },
    searchAirports(query) {
      let filteredItems = [];
      for(let i = 0; i < this.items.length; i++) {
        let item = this.items[i];
        if (item.iata.toLowerCase().indexOf(query.toLowerCase()) > -1 | item.airport.toLowerCase().indexOf(query.toLowerCase()) > -1 ) {
          filteredItems.push(item);
        }
      }
      return filteredItems;
    },
    itemProjectionFunction(item) {
      return item.airport + ' (' + item.iata + ')';
    }
  }
}
</script>

<style lang="scss">
  $form-max: 100%;
  $grey: #f5f7f9;
  $yellow: #ffd100;
  .calculate-form {
    display: flex;
    flex-wrap: wrap;
    margin-bottom: 40px;
    max-width: $form-max;
  }
  .form {
    &-group {
      margin-right: 20px;
      flex: 1;
      display: flex;
      border: 1px solid #cecece;
      border-radius: 10px;
      position: relative;
      &:last-child {
        margin-right: 0;
      }
    }
    &-label {
      border-radius: 8px 0 0 8px;
      padding: 10px;
      background-color: #e3e3e3;
    }
    &-input {
      width: 100%;
      input {
        max-width: 100%;
        width: 100%;
        padding: 12px 10px;
        font-size: 16px;
        outline: none;
      }
    }
    &-button {
      margin: auto 0 0 auto;
    }
  }
  .calculate-result {
    display: inline-flex;
    justify-content: center;
    align-items: flex-end;
    font-size: 16px;
    letter-spacing: 0.2px;
    flex-wrap: wrap;

    &-value {
      color: #e00505;
      font-size: 20px;
      padding-left: 10px;
      padding-right: 10px;
      line-height: 1;
      font-weight: bold;
    }
  }
  .result-wrapper {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    justify-content: center;
    flex-direction: column;

    .v-enter-active,
    .v-leave-active {
      transition: opacity 0.7s ease 1s;
    }

    .v-enter-from,
    .v-leave-to {
      opacity: 0;
    }
  }
  .calculate-result {
    margin-bottom: 30px;
  }
  .result-donate {
    display: flex;
    flex-direction: column;
    align-items: center;

    &-msg {
      font-weight: bold;
      padding-right: 20px;
      padding-top: 20px;
      font-size: 14px;
    }
  }
  .calculate-checkbox {
    &-input {
      display: none;
    }
    &-label {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 40px;
      height: 40px;
      background-color: #e3e3e3;
      border-radius: 10px;
      padding: 10px;
      cursor: pointer;
      opacity: 1;
      transition: all 0.3s;

      &:hover {
        opacity: 0.8;
      }

      svg {
        width: 25px;
        max-height: 100%;
      }
    }
  }
  .checkbox-group {
    margin-right: 20px;
    align-self: center;
  }
  .icon {
    svg {
      width: 100%;
      height: 100%;
    }
    &-plane {
      width: 40px;
      height: 100%;

      &.reverse {
        svg {
          backface-visibility: hidden;
          -webkit-font-smoothing: subpixel-antialiased;
          transform: rotate(45deg);
          transform-origin: 50% 50%;
        }
      }
    }
  }
  .p-autocomplete {
    max-width: 100%;
    display: inline-flex;
  }
  .p-autocomplete-panel {
    background-color: #fff;
    font-family: inherit;
  }
  .p-autocomplete-item {
    padding: 5px 3px;
    font-size: 16px;
    border-bottom: 1px solid #e3e3e3;
    opacity: .7;

    &:hover {
      opacity: 1;
    }
  }

  @media screen and (max-width: 768px) {
    .calculate-form {
      flex-direction: column;
      align-content: center;
      margin-bottom: 20px;
    }
    .form-group {
      margin: 0 0 20px 0;
      width: 100%;
      align-items: stretch;
    }
    .form-input input {
      padding: 10px;
    }
    .checkbox-group {
      margin-right: 0;
    }
    .calculate-checkbox-label {
      margin: 0 auto 20px;
    }
    .result-donate {
      flex-direction: column;

      &-msg {
        padding: 0 0 20px;
      }
    }
  }
</style>
