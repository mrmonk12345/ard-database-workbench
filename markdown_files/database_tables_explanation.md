### Database Tables Explanation

#### Projects



A study or research project.



* project\_id: auto-incrementing ID
* label: short label for quick identification
* prjna: project number in NCBI, if there is one
* article\_identifier: paper name + author and year
* article\_file\_name: associated publication file
* notes: additional project notes
* amplicon\_type\_id: default amplicon type used in the project



#### Amplicon Types



Defines the genetic region targeted for sequencing.



* amplicon\_type\_id: auto-incrementing ID
* marker\_gene: marker gene (e.g., 16S, ITS)
* variable\_region: target variable region
* amplicon\_length: amplicon length based on f and r lengths
* f\_name: forward primer name
* f\_sequence: forward primer sequence
* f\_length: forward primer length
* r\_name: reverse primer name
* r\_sequence: reverse primer sequence
* r\_length: reverse primer length



#### Project Amplicon Types



Associates projects with amplicon types.



* project\_id: project
* amplicon\_type\_id: amplicon type
* role: purpose or role of the amplicon type within the project



#### Sequencing Runs



A sequencing experiment run. needed for denoising.



* sequencing\_run\_id: auto-incrementing ID
* project\_id: associated project
* platform: sequencing platform
* run\_date: sequencing date
* depth: sequencing depth
* read\_type: single-end or paired-end
* notes: additional notes



#### Sequencing Outputs



Raw sequencing files generated from a sequencing run.



* sequencing\_output\_id: auto-incrementing ID
* label: label of the output, should be based on sample\_label
* project\_id: associated project
* sample\_id: sample
* sequencing\_run\_id: sequencing run
* amplicon\_type\_id: amplicon type
* srr: NCBI SRA accession
* fastq1: path or name of forward FASTQ file
* fastq2: path or name of reverse FASTQ file
* files\_origin: source of the files
* notes: additional notes
* zzz\_legacy\_library\_id: legacy reference



#### Libraries



Represents a prepared sequencing library (sample + amplicon\_type).



* library\_id: auto-incrementing ID
* label: library name
* sample\_id: associated sample
* amplicon\_type\_id: amplicon type
* notes: additional notes
* srx: SRA accession
* zzz\_legacy\_library\_id: legacy reference



#### Analysis Datasets



Datasets prepared for bioinformatic analysis. sets of analysis units with  the same amplicon type and sequencing run.



* analysis\_dataset\_id: auto-incrementing ID
* amplicon\_type\_id: amplicon type
* sequencing\_run\_id: sequencing run
* type: dataset type, should be base
* notes: additional notes



#### Analysis Units



A logical unit used in downstream data analysis.



* analysis\_unit\_id: auto-incrementing ID
* analysis\_unit\_name: name, should be: sample{sample\_id)\_AU{analysis\_unit\_id}
* label: label, should be based on smaple\_label
* library\_id: source library
* sequencing\_run\_id: sequencing run
* analysis\_dataset\_id: analysis dataset



#### Analysis Unit Files



Files associated with an analysis unit.



* analysis\_unit\_id: analysis unit
* sequencing\_output\_id: source sequencing output
* amplicon\_separating\_done: amplicon separation completed or not
* demultiplexing\_done: demultiplexing completed or not
* gzip\_done: compression completed or not
* read1\_path: forward read file path
* read2\_path: reverse read file path



#### Pipeline Definitions



Definitions of bioinformatic pipelines.



* pipeline\_definition\_id: auto-incrementing ID
* pipeline\_name: pipeline name
* pipeline\_version: pipeline version
* workflow\_name: workflow name
* workflow\_version: workflow version
* method\_name: analysis method
* method\_version: method version
* parameters: pipeline parameters



#### Pipeline Runs



Execution records of bioinformatic pipelines.



* pipeline\_run\_id: auto-incrementing ID
* pipeline\_definition\_id: pipeline definition
* analysis\_dataset\_id: analyzed dataset
* status: execution status
* trunc\_len\_f: forward read truncation length
* trunc\_len\_r: reverse read truncation length
* p\_min\_overlap: minimum overlap
* p\_max\_ee\_f: maximum expected errors (forward)
* p\_max\_ee\_r: maximum expected errors (reverse)
* sampling\_depth: rarefaction depth
* max\_depth: maximum sequencing depth
* processed\_data\_path: processed results location
* is\_primary: marks primary pipeline run
* notes: additional notes



#### ASVs



Amplicon Sequence Variants produced by a pipeline run.



* asv\_id: auto-incrementing ID
* pipeline\_run\_id: generating pipeline run
* sequence: ASV nucleotide sequence
* sequence\_hash: sequence hash or fingerprint



#### Feature Counts



Abundance counts of ASVs in analysis units.



* asv\_id: ASV
* analysis\_unit\_id: analysis unit
* pipeline\_run\_id: pipeline run
* sample\_id: sample
* count: observed abundance



#### Taxonomy



Taxonomic classification assigned to ASVs.



* asv\_id: ASV
* kingdom: kingdom classification
* phylum: phylum classification
* class: class classification
* order: order classification
* family: family classification
* genus: genus classification
* species: species classification
* confidence: assignment confidence
* reference\_db: taxonomy reference database
* date\_classified: classification date



#### Samples



Biological samples collected during a project.



* sample\_id: auto-incrementing ID
* sample\_name: internal sample name
* original\_sample\_label: original submitted identifier
* label: display label
* project\_id: project
* location\_id: collection location
* rootstock\_id: rootstock
* sampling\_compartment\_id: sampled compartment such as: rhizosphere, bulk soil, root tissue, ...
* treatment\_id: treatment applied
* time\_since\_planting: duration such as: '5 weeks', '2 days'
* replicate\_number: biological replicate
* initial\_health\_status: health status before treatment
* final\_health\_status: health status after treatment
* host\_species: host species
* scion\_cultivar: scion cultivar
* soil\_texture: soil texture: sandy, loamy, etc...
* soil\_type: soil type
* sampling\_depth: sampling depth in cm
* experimental\_setting: greenhouse, field, urban, etc...



#### Locations



Collection sites.



* location\_id: auto-incrementing ID
* label: location label
* country: country
* city: city
* coordinates: geographic coordinates



#### Rootstocks



Rootstock information.



* rootstock\_id: auto-incrementing ID
* name: rootstock name
* label: short label
* rootstock\_type: whether its resistant or susceptible or whatever
* description: description



#### Sampling Compartments



Plant or environmental compartments sampled.



* sampling\_compartment\_id: auto-incrementing ID
* name: compartment name
* label: short label
* description: description
* project\_id: project



#### Treatments



Experimental treatments.



* treatment\_id: auto-incrementing ID
* name: treatment name
* label: short label
* description: treatment description
* project\_id: project
* treatment\_function: intended function



#### Treatment Elements



Components that can be used in treatments.



* treatment\_element\_id: auto-incrementing ID
* name: element name
* category: category
* type: type
* subtype: subtype
* notes: notes



#### Treatment Element Assignments



Assignment of treatment elements to treatments.



* treatment\_id: treatment
* treatment\_element\_id: treatment element
* dose\_value: dose amount
* dose\_unit: dose units
* duration\_value: duration amount
* duration\_unit: duration units
* application\_method: method of application
* function: role within treatment
* notes: additional notes

