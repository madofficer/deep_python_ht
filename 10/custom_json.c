#include <Python.h>
#include <stdio.h>
#include <string.h>

static PyObject* custom_json_loads(PyObject* self, PyObject* args) {
    const char* json_str;

    if (!PyArg_ParseTuple(args, "s", &json_str)) {
        return NULL;
    }

    PyObject* json_module = PyImport_ImportModule("json");
    if (!json_module) {
        PyErr_SetString(PyExc_ImportError, "Failed to import 'json' module");
        return NULL;
    }

    PyObject* loads_func = PyObject_GetAttrString(json_module, "loads");
    if (!loads_func || !PyCallable_Check(loads_func)) {
        PyErr_SetString(PyExc_AttributeError, "Failed to get 'loads' function from 'json' module");
        Py_DECREF(json_module);
        return NULL;
    }

    PyObject* result = PyObject_CallFunction(loads_func, "s", json_str);

    Py_DECREF(loads_func);
    Py_DECREF(json_module);

    return result;
}


static PyObject* custom_json_dumps(PyObject* self, PyObject* args) {
    PyObject* dict;

    if (!PyArg_ParseTuple(args, "O!", &PyDict_Type, &dict)) {
        return NULL;
    }

    PyObject* json_module = PyImport_ImportModule("json");
    if (!json_module) {
        PyErr_SetString(PyExc_ImportError, "Failed to import 'json' module");
        return NULL;
    }

    PyObject* dumps_func = PyObject_GetAttrString(json_module, "dumps");
    if (!dumps_func || !PyCallable_Check(dumps_func)) {
        Py_DECREF(json_module);
        PyErr_SetString(PyExc_AttributeError, "Failed to get 'dumps' function from 'json' module");
        return NULL;
    }

    PyObject* kwargs = Py_BuildValue("{s:(s,s)}", "separators", ", ", ": ");
    if (!kwargs) {
        Py_DECREF(json_module);
        Py_DECREF(dumps_func);
        return NULL;
    }

    PyObject* result = PyObject_Call(dumps_func, PyTuple_Pack(1, dict), kwargs);

    Py_DECREF(kwargs);
    Py_DECREF(dumps_func);
    Py_DECREF(json_module);

    return result;
}



static PyMethodDef CustomJsonMethods[] = {
    {"loads", custom_json_loads, METH_VARARGS, "Parse a JSON string into a Python dictionary."},
    {"dumps", custom_json_dumps, METH_VARARGS, "Serialize a Python dictionary into a JSON string."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef custom_json_module = {
    PyModuleDef_HEAD_INIT,
    "custom_json",
    "Custom JSON parser and serializer.",
    -1,
    CustomJsonMethods
};

PyMODINIT_FUNC PyInit_custom_json(void) {
    return PyModule_Create(&custom_json_module);
}
