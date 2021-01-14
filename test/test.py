#!/bin/bash
find . -iname '*.txt' -printf "%s %p\0" | sort -z -k1rn \
	| while read -r -d $'\0' size file; do
		echo "Filnavn: $file, size: $size"
		while true; do
			read -p "Vil du slette (1) denne filen, gå videre (2) eller avslutte (0)?" REPLY
			case "$REPLY" in
				1) rm "$file"
					"$file slettet."
					;;
				2) continue ;;
				0) exit ;;
				#*) echo "Vennligst velg en av alternativene over.";;
			esac
		done
	 done
echo "Ferdig."


