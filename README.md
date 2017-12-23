
Fuzzy search for Alfred 3
=========================

`fuzzy.py` is a helper script for Alfred 3 Script Filters that replaces the "Alfred filters results" option with fuzzy search (Alfred uses "word starts with").

![](./demo.gif "")

How it works
------------

Instead of calling your script directly, you call it via `fuzzy.py`, which caches your script's output for the duration of the user session (as long as the user is using your workflow), and filters the items emitted by your script against the user's query using a fuzzy algorithm.

The query is compared to each item's `matches` field if it's present, and against the item's `title` field if not.


Example usage
-------------

`fuzzy.py` only works in Script Filters, and you should run it as a bash/zsh script (i.e. with `Language = /bin/bash` or `Language = /bin/zsh`).

Instead of running your own script directly, place `./fuzzy.py` in front of it.

For example, if your Script Filter script looks like this:

```bash
/usr/bin/python myscript.py
```

You would replace it with:

```bash
# Export user query to `query` environment variable, so `fuzzy.py` can read it
export query="$1"
# Or if you're using "with input as {query}"
# export query="{query}"

# call your original script via `fuzzy.py`
./fuzzy.py /usr/bin/python myscript.py
```

**Note**: Don't forget to turn off "Alfred filters results"!


Demo
----

Grab the [Fuzzy-Demo.alfredworkflow][demo] file from this repo to try out the search and view an example implementation.


Caveats
-------

Fuzzy search, and this implementation in particular, are by no means the "search algorithm to end all algorithms".


### Performance ###

By dint of being written in Python and using a more complex algorithm, `fuzzy.py` can only comfortably handle a small fraction of the number of results that Alfred's native search can. On my 2012 MBA, it becomes noticeably, but not annoyingly, sluggist at about ~2500 items.

If the script is well-received, I'll reimplement it in a compiled language. My [Go library for Alfred workflows][awgo] uses the same algorithm, and can comfortably handle 20K+ items.


### Utility ###

Fuzzy search is awesome for some datasets, but fairly sucks for others. It can work very, very well when you only want to search one field, such as name/title or filename/filepath, but it tends to provide sub-optimal results when searching across multiple fields, especially keywords/tags.

In such cases, you'll usually get better results from a word-based search.


Technical details
-----------------

The fuzzy algorithm is taken from [this gist][pyversion] by [@menzenski][menzenski], which is based on Forrest Smith's [reverse engineering of Sublime Text's algorithm][forrest].

The only addition is smarter handling of non-ASCII. If the user's query contains only ASCII, the search is diacritic-insensitive. If the query contains non-ASCII, the search considers diacritics.


Customisation
-------------

You can tweak the algorithm by altering the bonuses and penalties applied, or changing the characters treated as separators.

Export different values for the following environment variables before calling `fuzzy.py` to configure the fuzzy algorithm:

|       Variable      |  Default  |                  Description                  |
|---------------------|-----------|-----------------------------------------------|
| `adj_bonus`         | 5         | Bonus for adjacent matches                    |
| `camel_bonus`       | 10        | Bonus if match is uppercase                   |
| `sep_bonus`         | 10        | Bonus if after a separator                    |
| `unmatched_penalty` | -1        | Penalty for each unmatched character          |
| `lead_penalty`      | -3        | Penalty for each character before first match |
| `max_lead_penalty`  | -9        | Maximum total `lead_penalty`                  |
| `separators`        | `_-.([/ ` | Characters to consider separators (for the purposes of assigning `sep_bonus`)                                              |


Thanks
------

The fuzzy matching code was (mostly) written by [@menzenski][menzenski] and the algorithm was designed by [@forrestthewoods][forrestthewoods].


[awgo]: https://github.com/deanishe/awgo
[demo]: ./Fuzzy-Demo-0.2.alfredworkflow
[forrest]: https://blog.forrestthewoods.com/reverse-engineering-sublime-text-s-fuzzy-match-4cffeed33fdb
[forrestthewoods]: https://github.com/forrestthewoods
[menzenski]: https://github.com/menzenski
[pyversion]: https://gist.github.com/menzenski/f0f846a254d269bd567e2160485f4b89
