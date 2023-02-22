### ANNOTATE MANIFESTS FOR UPLOAD OF PUBLIC MAGS AND BINS #####

Python script to annotate the manifests files (generated using genome_uploader.py) for submission of co-assembled MAGs and BINS in fasta fromat to ENA (European Nucleotide Archive). The script generates the manifests necessary for submission with webin-cli.  

#Input:

The manifest_annotation.py takes as input one tsv (tab-separated values) table expecting the following columns:
  * _genome_name_: genome id (unique string identifier, shorter than 20 characters)
  * _accessions_: run(s) or assembly(ies) the genome was generated from (DRR/ERR/SRRxxxxxx for runs, DRZ/ERZ/SRZxxxxxx for assemblies). Genomes generated from a co-assembly of multiple runs needs to be separated comma(s).
  * _assembly_software_: assemblerName_vX.X
  * _binning_software_: binnerName_vX.X
  * _binning_parameters_: binning parameters
  * _stats_generation_software_: software_vX.X
  * _completeness_: `float`
  * _contamination_: `float`
  * _rRNA_presence_: `True/False` if 5S, 16S, and 23S genes, and at least 18 tRNA genes, have been detected in the genome
  * _NCBI_lineage_: full NCBI lineage, either in tax ids (`integers`) or `strings`. Format: x;y;z;...
  * _metagenome_: needs to be listed in the taxonomy tree [here](<https://www.ebi.ac.uk/ena/browser/view/408169?show=tax-tree>) (you might need to press "Tax tree - Show" in the right most section of the page)
  * _co-assembly_: `True/False`, whether the genome was generated from a co-assembly. N.B. the script only supports co-assemblies generated from the same project.
  * _genome_coverage_ : genome coverage against raw reads
  * _genome_path_: path to genome to upload (already compressed)
  * _broad_environment_: `string` (explanation following)
  * _local_environment_: `string` (explanation following)
  * _environmental_medium_: `string` (explanation following)

According to ENA checklist's guidelines, 'broad_environment' describes the broad ecological context of a sample - desert, taiga, coral reef, ... 'local_environment' is more local - lake, harbour, cliff, ... 'environmental_medium' is either the material displaced by the sample, or the one in which the sample was embedded prior to the sampling event - air, soil, water, ... For host-associated metagenomic samples, the three variables can be defined similarly to the following example for the chicken gut metagenome: "chicken digestive system", "digestive tube", "caecum". More information can be found at ERC000050 for bins and ERC000047 for MAGs under field names "broad-scale environmental context", "local environmental context", "environmental medium"

### How to Run ### 
The script needs an input tsv file of the METADATA of all MAGs or bins, and a path to all the manifest files generated using the genomes_uploader.py script.
