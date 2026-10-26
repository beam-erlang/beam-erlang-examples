%% SPDX-License-Identifier: Apache-2.0
-module(example_script).
-export([main/1]).

main(Args) ->
    io:format("Args: ~tp~n", [Args]).
