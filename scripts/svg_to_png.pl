#!/usr/bin/env perl

use strict;
use warnings;
use Path::Class;
use Capture::Tiny qw(capture);
my $inkscape = 'inkscape';

my $width = shift @ARGV or die "USAGE: $0 [width]\n";

my $src = dir('svg');
my $out = dir('images_temp');

$out->rmtree;
$out->mkpath;

while ( my $file = $src->next ) {
    next unless -f $file;
    my $name = $file->basename;
    if ( $name =~ s/\.svg$// ) {
        print "$name.svg -> $name.png\n";
        my ( $stdout, $stderr, $exit ) = capture {
            system( $inkscape, '--export-png', $out->file("$name.png"),
                '-w', $width, $file );
        };
        if ($exit) {
            die "Couldn't convert $file: $stderr\n";
        }
    }
    else {
        print "Skipping: $name\n";
    }
}
