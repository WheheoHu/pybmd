{{ objname | escape | underline}}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}
   :members:            
   :show-inheritance:   
   :inherited-members: 
   :noindex: 
   
   
   {% block methods %}


   {% if methods %}
   .. rubric:: {{ _('Methods') }}
   
   .. autosummary::
      :template: method.rst
      :toctree:
      
   {% for item in methods %}
      ~{{ name }}.{{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block attributes %}
   {% if attributes %}
   .. rubric:: {{ _('Attributes') }}

   .. autosummary::
      :toctree:
   {% for item in attributes %}
      ~{{ name }}.{{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}
