# **Design Philosophy of ARD Database**





important parts:



* sample metadata
* count table







##### types of metadata:





###### WHEN?



* Temporal data

  * Absolute: date and time
  * Relative: time since a defined event
  * Descriptive: season, growth stage





###### WHAT?



* Experimental context

  * What was done?
  * What was chosen by the researcher?



* Biological context

  * What was observed?





###### WHERE?



* Spatial data

  * Coordinates
  * Country
  * Location name



* Environmental data

  * Soil texture
  * Climate zone





###### HOW?



* Methods

  * Sampling





there could be elements that are both environmental data and experimental context, environmental factors chosen specifically by the researcher.



\####################################



sample metadata columns in current DB:



WHEN:



* Temporal Data

  * time\_since\_planting



WHAT:



* Experimental Context

  * treatment\_id
  * initial\_health\_status
  * experimental\_setting (greenhose pot, field, etc)



* Biological Context

  * final\_health\_status



WHERE?



* Spatial data

  * location\_id



* Environmental data

  * soil\_texture
  * soil\_type





HOW?



* Methods

  * sampling\_compartment
  * sampling\_depth









##### Data Organization



This document maps the architectural layers of the multi-omics microbiome database schema. It details how the system categorizes metadata and highlights the parallel relationship between raw incoming data and structured analytical targets.



###### 1\. Categorization of Database Tables

The database is organized into distinct operational zones, tracking data from its physical ecosystem origin up to structured bioinformatic matrix outputs.



###### Biological Metadata (The Physical Layer)

These tables capture the experimental setup and the environmental/biological reality of the samples before any sequencing occurs.

* Tables: projects, samples, libraries, rootstocks, locations, treatments, sampling\_compartments.
* Purpose: Tracks the origin, environmental conditions, host genetics, and extraction properties of the physical biomass.



###### Technical \& Ingestion Metadata (The Input Layer)

These tables anchor physical assets and technical laboratory details to the sequencing event.

* Tables: sequencing\_runs, sequencing\_run\_libraries, library\_amplicon\_types.
* Purpose: Tracks platform mechanics, barcodes/indices, and run parameters, serving as the technical context.



###### System Axes (The Definition Layer)

* Table: amplicon\_type.
* Purpose: Defines the biological target (e.g., 16S, ITS, region, primer sequences). It acts as a global look-up table used by all other layers to ensure scientific validity.



###### Operational \& Pipeline Metadata (The Execution Layer)

These tables manage active bioinformatic processing (e.g., QIIME2/DADA2 pipelines).

* Tables: analysis\_units, analysis\_datasets, analysis\_datasets\_input, pipeline\_runs.
* Purpose: Groups data uniformly to execute tools with identical parameters and error models.



###### Result Metadata (The Resolution Layer)

These tables capture downstream abundance matrices and taxonomy metrics after pipeline execution.

* Tables: feature\_counts, asvs, taxonomy.
* Purpose: Resolves batch-processed outputs back into granular, sample-specific tables.







###### 2\. The Core Parallel Architecture: Sequencing Outputs vs. Analysis Units

The defining feature of this schema is the parallel, decoupled relationship between 'sequencing\_outputs' and 'analysis\_units'. This design addresses a major hurdle in bioinformatics: raw data files delivered from facilities rarely match downstream analysis requirements perfectly.



###### Sequencing Outputs: The Raw Data Layer

The 'sequencing\_outputs' table represents unconstrained physical files (e.g., FASTQ, SRR).

* Attributes like sequencing\_run\_id, library\_id, and amplicon\_type\_id are intentionally nullable.
* This flexibility allows the database to ingest data exactly as it arrives from a facility, regardless of format:

  * A single file containing an entire multiplexed run (sequencing\_run\_id only).
  * A file pre-sorted by sample but containing multiple primer sets (sequencing\_run\_id + library\_id).
  * A fully demultiplexed target file (sequencing\_run\_id + library\_id + amplicon\_type\_id).



###### Analysis Units: The Structured Target Layer

The 'analysis\_units' table represents the strict technical coordinate required for downstream pipelines. Unlike raw files, it requires complete structure.

* Every analysis unit must have an explicit, non-null triad: Sequencing Run + Library + Amplicon Type.
* It defines exactly what *should* be analyzed, providing a clean, predictable, and fully verified record for downstream code.



###### Why This Parallel Structure Matters

By decoupling raw file tracking from pipeline execution, the schema achieves three critical goals:

1. Asynchronous Ingestion: You can register messy incoming files immediately without waiting to resolve index hoppings, multiplex issues, or misnamed samples at the application layer.
2. Arbitrary Reconstitution: If a raw sequencing file needs to be re-parsed, split, or combined, you alter the 'sequencing\_outputs' mapping without breaking the downstream 'analysis\_units' history or their associated results.
3. Strict Pipeline Validation: The 'analysis\_units' table uses the lab's junction tables (sequencing\_run\_libraries and library\_amplicon\_types) as a firewall. It guarantees that a bioinformatic execution path cannot exist unless the physical pooling and target assays actually happened at the wet-lab bench.

