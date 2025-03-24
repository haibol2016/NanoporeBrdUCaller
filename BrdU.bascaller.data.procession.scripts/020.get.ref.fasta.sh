samtools view -bh -q 60  FAS54789_pass_barcode01_dc523426_25_dorado.sam > FAS54789_pass_barcode01_dc523426_25_dorado.mapq60.bam

bedtools bamtobed -i FAS54789_pass_barcode02_dc523426_14_dorado.mapq60.bam |bedtools getfasta -fi ../../docs/Homo_sapiens-GCA_009914755.4-T2T-unmasked.fa -bed - -s -name > FAS54789_pass_barcode02_dc523426_14_dorado.mapq60.ref.fasta

