import numpy as np
import pandas as pd
import glob
import os

#headers
vcf_columns = ['Chr', 'Start', 'End', 'Ref', 'Alt', 'Func.refGene', 'Gene.refGene',
       'GeneDetail.refGene', 'ExonicFunc.refGene', 'AAChange.refGene',
       'cytoBand', 'ExAC_ALL', 'ExAC_AFR', 'ExAC_AMR', 'ExAC_EAS', 'ExAC_FIN',
       'ExAC_NFE', 'ExAC_OTH', 'ExAC_SAS', 'gnomAD_exome_ALL',
       'gnomAD_exome_AFR', 'gnomAD_exome_AMR', 'gnomAD_exome_ASJ',
       'gnomAD_exome_EAS', 'gnomAD_exome_FIN', 'gnomAD_exome_NFE',
       'gnomAD_exome_OTH', 'gnomAD_exome_SAS', 'gnomAD_genome_ALL',
       'gnomAD_genome_AFR', 'gnomAD_genome_AMR', 'gnomAD_genome_ASJ',
       'gnomAD_genome_EAS', 'gnomAD_genome_FIN', 'gnomAD_genome_NFE',
       'gnomAD_genome_OTH', 'Kaviar_AF', 'Kaviar_AC', 'Kaviar_AN', 'CLINSIG',
       'CLNDBN', 'CLNACC', 'CLNDSDB', 'CLNDSDBID', 'avsnp147', 'SIFT_score',
       'SIFT_pred', 'Polyphen2_HDIV_score', 'Polyphen2_HDIV_pred',
       'Polyphen2_HVAR_score', 'Polyphen2_HVAR_pred', 'LRT_score', 'LRT_pred',
       'MutationTaster_score', 'MutationTaster_pred', 'MutationAssessor_score',
       'MutationAssessor_pred', 'FATHMM_score', 'FATHMM_pred', 'PROVEAN_score',
       'PROVEAN_pred', 'VEST3_score', 'CADD_raw', 'CADD_phred', 'DANN_score',
       'fathmm-MKL_coding_score', 'fathmm-MKL_coding_pred', 'MetaSVM_score',
       'MetaSVM_pred', 'MetaLR_score', 'MetaLR_pred',
       'integrated_fitCons_score', 'integrated_confidence_value', 'GERP++_RS',
       'phyloP7way_vertebrate', 'phyloP20way_mammalian',
       'phastCons7way_vertebrate', 'phastCons20way_mammalian',
       'SiPhy_29way_logOdds', 'Otherinfo', 'Unnamed: 80', 'Unnamed: 81',
       'Unnamed: 82', 'Unnamed: 83', 'Unnamed: 84', 'Unnamed: 85',
       'Unnamed: 86', 'Unnamed: 87', 'Unnamed: 88', 'Unnamed: 89',
       'Unnamed: 90', 'Unnamed: 91']

file_path = "/Users/matthewpozsgai/Desktop/"
filter_path = "/Users/matthewpozsgai/Desktop/prioritized_genes.csv"

#read in filter file as series
filter_by = pd.read_csv(filter_path, dtype = str, squeeze = True)

for filename in glob.glob(os.path.join(file_path, '*.txt')):

    #read in txt as a dataframe
    unfiltered = pd.read_csv(filename, delimiter = '\t',dtype = str, names = vcf_columns, lineterminator = "\n", header = 0)

    #replace empty population frequencies with zero
    unfiltered["gnomAD_genome_ALL"] = unfiltered["gnomAD_genome_ALL"].replace('.', 0)

    #convert population frequencies to integer values in order to filter
    unfiltered["gnomAD_genome_ALL"] = unfiltered["gnomAD_genome_ALL"].apply(pd.to_numeric)

    #list of genes to keep intronic variants
    keep_intronic = ["GATA2", "FANCI", "BRCA1", "BRCA2", "NF1","IKZF1"]

    #remove intronic variants except for keep_intronic list
    mask = (unfiltered['Func.refGene'] == "intronic") & (~unfiltered['Gene.refGene'].isin(keep_intronic))
    intronic_filtered = unfiltered[~mask]

    #select rows from unfiltered where the string based on mutation type and population frequency
    pop_filtered = intronic_filtered.loc[(intronic_filtered['gnomAD_genome_ALL'] <= .005)]

    #filter by gene in pirority list
    gene_filtered = pop_filtered.loc[pop_filtered['Gene.refGene'].isin(filter_by)]

    #calculate vaf of remaining variants and add it to a new column
    gene_filtered["ref"] = gene_filtered["Unnamed: 91"].apply(lambda x : x.split(":")[1].split(",")[0])
    gene_filtered["alt"] = gene_filtered["Unnamed: 91"].apply(lambda x : x.split(":")[1].split(",")[1])
    gene_filtered["depth"] = gene_filtered["Unnamed: 91"].apply(lambda x : x.split(":")[2])
    gene_filtered["alt"] = gene_filtered["alt"].apply(pd.to_numeric)
    gene_filtered["depth"] = gene_filtered["depth"].apply(pd.to_numeric)
    gene_filtered["vaf"] = gene_filtered["alt"]/gene_filtered["depth"]

    #reorder dataframe columns
    cols = list(gene_filtered.columns)
    cols = [cols[-1]] + cols[:-1]
    gene_filtered = gene_filtered[cols]
    gene_filtered.insert(0, column = "Notes", value = "")

    #write to excel
    output_file = str(filename).replace('hg38_multianno.txt', 'priority_filter.xlsx')
    writer = pd.ExcelWriter(output_file)
    gene_filtered.to_excel(writer,'Filterd')
    writer.save()
