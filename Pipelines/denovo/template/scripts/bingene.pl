#!/usr/bin/perl -w

###################################################################################################
#
# Name: bingene.pl
#
# This script is used to blast assembled sequences of each sample and bin sequences into genes.
#
# Datafile: fasta file of the query and fasta files of the samples
#
# Imput: the query name and list of subject taxon names
#
# Output: blastn output file in format 6, sequences binned as genes.
#
# Written by 
#                 Chenhong Li
#                 College of Charleston, USA.
#                 Created on Nov 2011
#                 Last modified on
#
###################################################################################################

use strict;
use warnings;
use extract; #module for extract sequences


use Getopt::Long;   # include the module for input


my $query; #variable for store query species name
my $subject; #list of subject name
my $MK = "N"; #default not make blast database
my $B = "N"; #default don't do blastn first
my $F = "N"; #default include flanking region
my $help;

my $opt = GetOptions( 'query:s', \$query,
                      'subject:s', \$subject,
                      'mk:s', \$MK,
                      'b:s', \$B,
                      'f:s', \$F,
                      'help!', \$help); #set command line options
                      

if (!($opt && $query) || $help) {#check for the required inputs
   print STDERR "\nExample usage:\n";
   print STDERR "$0 -query=\"Callorhinchus_milii\" -subject=\"Hydrolagus_affinis_1 Hydrolagus_affinis_2\"\n\n";
   print STDERR "Options:\n";
   print STDERR "        -query = name of the query species \n";
   print STDERR "        -subject = a list of subject species, use underscore to link genus and\n";
   print STDERR "                     species name; taxa seperated by one space\n";
   print STDERR "        -mk = N makeblastdb first, default is not (N)\n";
   print STDERR "        -b = N do blast first, default is not (N)\n";
   print STDERR "        -f = N include flanking sequences, default is not (N)\n\n";
   print STDERR "For more optional parameters, see README.txt\n\n";
   exit;
}


my @sub = split (/\s/, $subject); #split the names of refer genomes
chomp(@sub);
my @sortedsub = sort @sub;
        
if ($MK ne "N") {#if not N do makeblastdb first

    my ($OLD_FILE, $NEW_FILE, $INDEX_FILE);

    foreach my $sub (@sortedsub) {
        #call outside program makeblastdb
        `makeblastdb -in ../abyssout/$sub.fas -out ../blastdb/$sub -dbtype nucl`;

        my ($old, $new, $index);
    
        $old = "../abyssout/$sub.fas";
        $new = "../blastdb/$sub.new.fas";
        $index = "../blastdb/$sub.new.index";

        open $OLD_FILE, "<$old" or die ("Cannot open $old for reading ($!)");
        open $NEW_FILE, ">$new" or die ("Cannot open $new for writing ($!)");
        open $INDEX_FILE, ">$index" or die ("Cannot open $index for writing ($!)");

        my ($id, $seq);
        my $file_pointer = 0;
        while (my $line = readline ($OLD_FILE)) {
            chomp $line;
            if ($line =~ /^>/) { # if we find >
                if ($id) { # if id exists we first need to write old information
        		    print $INDEX_FILE "$id\t$file_pointer\n";
                    $file_pointer += length(">$id\n$seq\n");
        	        print $NEW_FILE ">$id\n$seq\n";
                } 
        	    # .. And then extract the new id and set sequence to empty
        	    ($id) = $line =~ /^>(\S+)/;
        	    $seq = "";
            } else {
        		    $seq .= $line;
            }
        }
        # We need to store the last sequence as well
        print $INDEX_FILE "$id\t$file_pointer\n";
        print $NEW_FILE ">$id\n$seq\n";

        close ($OLD_FILE) or die "Can't close the old file!!!";
        close ($NEW_FILE) or die "Can't close the new file!!!";
        close ($INDEX_FILE) or die "Can't close the new file!!!";

    }
}

if ($B ne "N") {#if not N do blast first
    #call outside program blastn
    foreach my $sub (@sortedsub) {
        `blastn -query ../query/$query.fas -db ../blastdb/$sub -out ../blastout/$sub.blast.out.txt -word_size 7 -gapopen 5 -gapextend 2 -penalty -1 -reward 1 -evalue 0.00000001 -outfmt 6`;
    }
}

#create files for each query genes

my $resultdir = $query . ".result";
`mkdir ../genebin/$resultdir`;#make dir for the output

my ($QUERY_FILE, $FASTA_FILE);
open $QUERY_FILE, "< ../query/$query.fas" or die ("Cannot open $query for reading ($!)");
while (my $line = readline ($QUERY_FILE)) {
    chomp $line;
    if ((my $gene) = $line =~ /^>(\S+)/) { # if we find >
        my $new = "../genebin/$resultdir/$gene.fas";
        open $FASTA_FILE, ">$new" or die ("Cannot open $new for writing ($!)");
        print $FASTA_FILE ">query$query\n";
        my $seqline = readline ($QUERY_FILE);
        print $FASTA_FILE "$seqline";
        close ($FASTA_FILE) or die "Can't close the fasta file!!!";        
    }
}
close ($QUERY_FILE) or die "Can't close the query file!!!";        

#retrieve gene sequences based on blast results
my $BLAST_FILE;

foreach my $sub (@sortedsub) {
    my $nextgene = "a";
    my $numofgene = 0;

    my $seqfile = "../blastdb/$sub.new.fas";
    my $indexfile = "../blastdb/$sub.new.index";
    my $blast = "../blastout/$sub.blast.out.txt";
    open $BLAST_FILE, "<$blast" or die ("Cannot open $blast for reading ($!)");
    
    while (my $line = readline ($BLAST_FILE)) {
        chomp $line;
        my ($gene, $seqid, $pos1, $pos2) = $line =~ /(\S+)\s+(\S+)\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+(\S+)\s+(\S+)\s+\S+\s+\S+/;
        $numofgene ++ if ($gene ne $nextgene);
        $nextgene = $gene;
        my $new = "../genebin/$resultdir/$gene.fas";
        open $FASTA_FILE, ">>$new" or die ("Cannot open $new for writing ($!)");
        my ($subseq, $strain) = &extract::extractseq($seqid, $pos1, $pos2, $seqfile, $indexfile, $F);
        print $FASTA_FILE ">$sub\n$subseq\n";
        close ($FASTA_FILE) or die "Can't close the fasta file!!!";

    }
    
    close ($BLAST_FILE) or die "Can't close the blast file";


    print "$sub has $numofgene gene captured\n"; #report how many genes have hits

}
