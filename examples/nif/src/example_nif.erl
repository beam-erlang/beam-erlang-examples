%% SPDX-License-Identifier: Apache-2.0
-module(example_nif).
-export([hello/0]).
-nifs([hello/0]).

hello() -> erlang:nif_error(nif_not_loaded).
