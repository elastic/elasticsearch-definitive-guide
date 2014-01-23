#!/usr/bin/env perl

use strict;
use warnings;

use Elasticsearch;

my $e = Elasticsearch->new(trace_to=>'Stderr');
$e->indices->delete( index => ['_all'], ignore => 404);

my @users = (
    {
        id    => 1,
        type  => 'user',
        index => 'us',
        body  => {
            name     => 'John Smith',
            username => '@john',
            email    => 'john@smith.com',
        }
    },
    {
        id    => 2,
        type  => 'user',
        index => 'gb',
        body  => {
            name     => 'Mary Jones',
            username => '@mary',
            email    => 'mary@jones.com'
        }
    },
);

my @tweets = (
    'Elasticsearch means full text search has never been so easy',
    'However did I manage before Elasticsearch?',
    "\@mary it is not just text, it does everything",
    "The Elasticsearch API is really easy to use",
    "The Query DSL is really powerful and flexible",
    "They have added did-you-mean suggest functionality to #elasticsearch",
    "Geo-location aggregations are really cool",
    "ElasticSearch surely is one of the hottest new NoSQL products",
    "Elasticsearch is built for the cloud, easy to scale",
    "ElasticSearch and I have left the honeymoon stage, and I still love her.",
    "So yes, I am an Elasticsearch fanboy",
    "How many more cheesy tweets do I have to write?",
);

my @docs = @users;
my $i    = 3;
while ( my $tweet = shift @tweets ) {
    my $user = $users[ $i % 2 ];
    push @docs,
        {
        index => $user->{index},
        type  => 'tweet',
        id    => $i,
        body  => {
            tweet => $tweet,
            date  => "2014-09-" . ( $i + 10 ),
            name => $user->{body}{name},
            user_id =>  1 + ( $i % 2 ),
        }
        };
    $i++;
}

$e->index( %$_ ) for @docs;

