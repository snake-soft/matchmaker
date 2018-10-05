def list_compare(old, new):
    """ return{'rem':[miss in new], 'add':[miss in old]} """
    #import pdb; pdb.set_trace()
    return {
        'rem': [x for x in old if x not in new],
        'add': [x for x in new if x not in old]
        }
