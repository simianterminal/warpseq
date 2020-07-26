from . exceptions import *

class BaseApi(object):

    def __init__(self, public_api, song):
        self.api  = public_api
        self.song = song

        #self.fn_name_lookup = getattr(self.song, self.__class__.name_lookup_method)


        if self.__class__.add_method:
            self.fn_add         = getattr(self.song, self.__class__.add_method)
        self.add_required   = self.__class__.add_required
        self.edit_required  = self.__class__.edit_required
        if self.__class__.remove_method:
            self.fn_remove      = getattr(self.song, self.__class__.remove_method)

        self.public_fields = self.__class__.public_fields

    def lookup(self, name, require=False):
        coll = self._get_collection()
        if self.__class__.storage_dict:
            for (k,v) in coll.items():
                if v.name == name:
                    return v
        else:
            for k in coll:
                if k.name == name:
                    return k
        if require:
            raise NotFound("\"%s\" not found" % name)
        return None

    def list(self):
        coll = self._get_collection()
        data = []
        # FIXME: will need modifications if storage_list is True
        for (k,v) in coll.items():
            data.append(v.name)
        return data


    def details(self, name):
        obj = self.lookup(name)
        if obj is None:
            raise NotFound("\"%s\" not found" % name)
        data = obj.to_dict()
        new_data = dict()
        for (k,v) in data.items():
            if k in self.public_fields:
                new_data[k] = v
        return new_data

    def _get_collection(self):
        return getattr(self.song, self.__class__.song_collection)

    def _require_input(self, what, params):
        for k in what:
            if params[k] is None:
                raise RequiredInput("%s is required" % k)

    def _ok(self):
        return True

    def _generic_add(self, name, params):
        obj = self.lookup(name)
        del params['self']
        del params['name']
        self._require_input(self.add_required, params)
        if not obj:
            obj = self.__class__.object_class(name=name, **params)
            self.fn_add([obj])
            return self._ok()
        else:
            raise AlreadyExists()

    def _generic_edit(self, name, params):
        obj = self.lookup(name)
        if not obj:
            raise NotFound("%s not found" % name)
        del params["name"]
        del params["self"]

        self._require_input(self.edit_required, params)
        if "new_name" in params:
            del params["new_name"]


        for (k,v) in params.items():
            value = v
            if v is not None:
                value = v
                if value == "":
                    value = None
                setattr(obj, k, value)
        return self._ok()

    def _generic_remove(self, name):
        obj = self.lookup(name)
        self.fn_remove(obj)
        return self._ok()

    def _generic_list_names(self):
        results = []
        coll = _get_collection()
        for (k,v) in coll:
            results.append(k.name)

    # NOT USED
    #def _generic_all(self):
    #    results = []
    #    coll = _get_collection()
    #    for (k,v) in coll:
    #        # TODO: we may want to trim this to just public data members
    #        results.append(v.to_json())
