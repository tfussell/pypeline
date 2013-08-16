package extract;

###################################################################################################
#
# Moduel name: extract
#
# This module is used to screen nuclear gene cds large than a value ($Lc) from genomic 
# sequences (EMBL flat file). Three sub routines are incluced: getcds, stack and extractseq.
#
# Datafile: a folder include all embl files of the query taxon, fasta files and index file of the
#           query genome.
#
# Imput: the query name and $Lc from main program.
#
# Output: a fasta query file including all merged CDS sequences larger than $Lc, listed in the
#         order of global position on chromosomes.
#
# Written by 
#                 Chenhong Li
#                 Univeristy of Nebraska - Lincoln, USA.
#                 Created on June 2010
#                 Last modified at
#
###################################################################################################

use strict;
use warnings;



###################################################################################################
#
# sub routine: extractseq
#
# This sub is used to extract the sequence from large fasta sequences.
#
# Imput data include the $seqid, $pos1 and $pos2.
#
# Return is the extracted sequence and the strand (+ or -).
#
###################################################################################################

sub extractseq {

    my $seqid = shift(@_); #get the $seqid from main program
    my $pos1 = shift(@_); #get the position 1
    my $pos2 = shift(@_); #get the position 2
    my $seqfile = shift(@_); #get the large fasta file name
    my $indexfile = shift(@_); #get the index file name
    my $F = shift(@_);

    my $seqlength = abs($pos1 - $pos2) + 1; #calculate the length of the seq
    
    my $strand = 1; 
    my $seqstart;
    
    if ($pos1 < $pos2) { #pick the small number as sequence start point
       $seqstart = $pos1;
    }
    elsif ($pos1 > $pos2) {
        $seqstart = $pos2;
        $strand = -1;
    }
    

    my ($SEQ_FILE, $INDEX_FILE);
    open ($SEQ_FILE, "<$seqfile") or die "Cannot open $seqfile for reading ($!)";
    open ($INDEX_FILE, "<$indexfile") or die "Cannot open $indexfile for reading ($!)";


    # First read the index file
    my %index;
    my $id;
    while (my $line = readline ($INDEX_FILE)) {
    	chomp $line;
    	my ($wholeid, $position) = split /\t/, $line;# the id in index file is longer than in embl file
    	if (($id) = $wholeid =~ /.+:(\S+):\d+:\d+:1$/) {
    	    $index{$id} = $position;
    	}
    	else {
    	    ($id) = $wholeid =~ /^(\S+).*/;
    	    $index{$id} = $position;
    	}
    }


    # and now we have superfast access to our sequences:
    seek $SEQ_FILE, $index{$seqid}, 0;  # letÕs jump to our seq
    readline($SEQ_FILE);  # first line is header, skip
    my $seq = readline($SEQ_FILE);	# second line is the whole sequence
    my $subseq = substr($seq, $seqstart, $seqlength); #get the substring

    if ($F ne "N") {#if we want retrive the whole sequence
        $subseq = $seq;
    }

    chomp $subseq;
    
    if ($strand == -1) { #reverse and complement the sequence if minus strand
        my $revsubseq = reverse $subseq;
        $revsubseq =~ tr/ACTGN/TGACN/;
        $subseq = $revsubseq;
    }

    close ($SEQ_FILE) or die "Can't close the new file!!!";
    close ($INDEX_FILE) or die "Can't close the index file!!!";

    return($subseq, $strand);
}







1
