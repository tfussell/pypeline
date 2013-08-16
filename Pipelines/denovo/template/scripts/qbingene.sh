#!/bin/sh
#$ -l mpi_available=1 -pe openmpi 4 -N cm
cd /NAS/groups/orti/bingenes/scripts

./bingene.pl -query "Callorhinchus_milii" -subject "Aetobatus_narinari Callorhinchus_milii Carcharhinus_amblyrhynchos Chlamydoselachus_anguineus Etmopterus_joungi Heterodontus_portusjacksoni Isurus_oxyrhinchus Leucoraja_erinacea Leucoraja_erinacea_gb Neotrygon_cf_kuhlii Orectolobus_halei Rhinobatos_schlegelii Squatina_nebulosa Torpedo_formosa" -mk=y -b=y -f=y > dirty13final.log.txt

./bingene.pl -query "Danio_rerio" -subject "Albula_vulpes Amia_calva Anguilla_rostrata Apteronotus_albifrons Chanos_chanos Dorosoma_cepedianum Elops_saurus Hiodon_alosoides Hypophthalmichthys_molitrix Ictalurus_punctatus Lepisosteus_platostomus Micropercops_swinhonis Osteoglossum_bicirrhosum Polyodon_spathula Polypterus_senegalus Pygocentrus_nattereri Rhinogobius_giurinus Saccopharynx_ampullaceus Scaphirhynchus_platorynchus Siniperca_chuatsi" -mk=y -b=y -f=y > basalactionps.log.txt

./bingene.pl -query "Callorhinchus_milii" -subject "Rhizoprionodon_170 Prionace_glauca_45 Negaprion_brevirostris_5559 Mustelus_canis_25 Mustelus_canis_22 Etmopterus_bullisi_5960 Chlamydoselachus_anguineus_Holo Carcharias_altimus_5558 Carcharhinus_plumbeus_20 Apristurus_manis_Am" -mk=y -b=y -f=y > formalin.log.txt