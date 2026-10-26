/* SPDX-License-Identifier: Apache-2.0 */
#include <erl_nif.h>
#include <string.h>

static ERL_NIF_TERM hello(ErlNifEnv *env, int argc, const ERL_NIF_TERM argv[])
{
    static const char greeting[] = "Hello, world!";
    ERL_NIF_TERM result;
    unsigned char *bytes;
    (void)argc;
    (void)argv;
    bytes = enif_make_new_binary(env, sizeof(greeting) - 1, &result);
    if (bytes == NULL) {
        return enif_raise_exception(env, enif_make_atom(env, "enomem"));
    }
    memcpy(bytes, greeting, sizeof(greeting) - 1);
    return result;
}

static ErlNifFunc functions[] = {{"hello", 0, hello, 0}};
ERL_NIF_INIT(example_nif, functions, NULL, NULL, NULL, NULL)
