from django.shortcuts import render
from django import forms
from Bio.Seq import Seq
from Bio.SeqUtils import molecular_weight
from Bio.SeqUtils.ProtParam import ProteinAnalysis

class SequenceForm(forms.Form):
    sequence = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 4, "cols": 40}),
        label="Enter DNA, RNA, or Protein Sequence",
        required=True
    )

def sequence_analysis(request):
    result = {}  # Initialize result dictionary
    error_message = None
    form = SequenceForm()

    if request.method == "POST":
        form = SequenceForm(request.POST)
        if form.is_valid():
            sequence = form.cleaned_data["sequence"].strip().upper()

            if not sequence:
                error_message = "Please enter a valid sequence."
            else:
                # Determine sequence type
                if set(sequence) <= {"A", "T", "G", "C"}:
                    seq_type = "DNA"
                elif set(sequence) <= {"A", "U", "G", "C"}:
                    seq_type = "RNA"
                elif set(sequence) <= {"A", "R", "N", "D", "C", "Q", "E", "G", "H", "I", "L", "K", "M", "F", "P", "S", "T", "W", "Y", "V"}:
                    seq_type = "Protein"
                else:
                    seq_type = "Unknown"

                if seq_type == "DNA":
                    bio_seq = Seq(sequence)
                    translation = bio_seq.translate(to_stop=True)

                    result = {
                        "Original Sequence": sequence,
                        "Reverse Complement": str(bio_seq.reverse_complement()),
                        "Transcription (RNA)": str(bio_seq.transcribe()),
                        "Translation (Protein)": str(translation)
                    }

                elif seq_type == "RNA":
                    bio_seq = Seq(sequence)
                    result = {
                        "Original Sequence": sequence,
                        "Reverse Complement": "N/A (RNA sequence)",
                        "Transcription (RNA)": "Already RNA",
                        "Translation (Protein)": str(bio_seq.translate(to_stop=True))
                    }

                elif seq_type == "Protein":
                    try:
                        analysis = ProteinAnalysis(sequence)
                        aa_composition = analysis.count_amino_acids()
                        molecular_wt = molecular_weight(sequence, seq_type="protein")
                        instability_index = analysis.instability_index()
                        gravy = analysis.gravy()

                        result = {
                            "Number of Amino Acids": len(sequence),
                            "Molecular Weight": round(molecular_wt, 2),
                            "Theoretical pI": round(analysis.isoelectric_point(), 2),
                            "Amino Acid Composition": aa_composition,
                            "Instability Index": round(instability_index, 2),
                            "Grand Average Hydropathicity (GRAVY)": round(gravy, 3)
                        }
                    except Exception as e:
                        error_message = f"Error analyzing protein sequence: {str(e)}"

                else:
                    error_message = "Invalid sequence format. Please enter a valid DNA, RNA, or Protein sequence."

            return render(request, "results.html", {"result": result, "error_message": error_message})

    return render(request, "index.html", {"form": form})
