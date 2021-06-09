// Global variables
var defaultValues = {
    
    Tagger: {
        halogenatedRegex: "([Ff]luor(?!ene)|[Cc]hlor(?!ophyl)|[Bb]rom|[Ii]od)",
        peptideRegex: "^(Ala|Arg|Asn|Asp|Cys|Gln|Glu|Gly|His|Ile|Leu|Lys|Met|Phe|Pro|Ser|Thr|Trp|Tyr|Val|[-\\s,]){3,}$",
    },

    REname: {
        removeRowRegex: "No compounds found for experimental mass",
        compoundSeparator: "\\s//\\s",
        aminoAcidSeparator: "\\s",
    },

    RowMerger: {
        comparedColumns: "",
        conservedColumns: "Identifier, Name",
    },

    TableMerger: {
        decimalPlaces: "4",
    },

    Ubiquitous: {
        filename: "", // Got from event defined in /assets/js/defaultOutputName.js
    }
    

};