/**
 * MUI WebComponents forms module
 * @module webcomponents/forms
 */

'use strict';


var jqLite = require('../js/lib/jqLite.js'),
    muiForms = require('../js/forms.js'),
    formControlTagName = muiForms.formControlClass;


/**
 * Class representing a FormControl element.
 * @class
 */
var FormControlProto = Object.create(HTMLElement.prototype);


/** FormControl createdCallback */
FormControlProto.createdCallback = function() {
  var root = this.createShadowRoot(),
      innerEl = document.createElement('div'),
      labelEl;

  var attrs = {
    type: this.getAttribute('type') || 'text',
    value: this.getAttribute('value'),
    placeholder: this.getAttribute('placeholder'),
    label: this.getAttribute('label'),
    floating: this.getAttribute('floating')
  };

  // create wrapper
  innerEl.setAttribute('class', muiForms.formGroupClass);

  // input element
  innerEl.appendChild(_createInputEl(attrs));

  // label element
  if (attrs.label) {
    var labelEl = _createLabelEl(attrs);
    innerEl.appendChild(labelEl);

    // add event listeners
    muiForms.initialize(labelEl);
  }

  // add to root
  root.appendChild(_getStyleEl().cloneNode(true));
  root.appendChild(innerEl);
}


// ------------------------------
// Utilities
// ------------------------------
var styleEl;


function _getStyleEl() {
  // get or create cached element
  if (styleEl === undefined) {
    styleEl = document.createElement('style');
    styleEl.innerHTML = require('mui.min.css');
  }

  return styleEl;
}


function _createInputEl(attrs) {
  var inputEl;

  // input element
  if (attrs.type === 'textarea') {
    inputEl = document.createElement('textarea');
    if (attrs.value) inputEl.appendChild(document.createTextNode(attrs.value));
  } else {
    inputEl = document.createElement('input');
    inputEl.setAttribute('type', attrs.type);
    if (attrs.value) inputEl.setAttribute('value', attrs.value);
  }

  if (attrs.placeholder) {
    inputEl.setAttribute('placeholder', attrs.placeholder);
  }

  inputEl.setAttribute('class', muiForms.formControlClass);

  return inputEl;
}


function _createLabelEl(attrs) {
  var labelEl = document.createElement('label');
  labelEl.appendChild(document.createTextNode(attrs.label));
  
  // configure floating label
  if (attrs.floating !== null) {
    labelEl.setAttribute('class', muiForms.floatingLabelBaseClass);
  }

  return labelEl;
}


/** Define module API */
module.exports = {
  /** Register module elements */
  registerElements: function() {
    var FormControlElement = document.registerElement(formControlTagName, {
      prototype: FormControlProto
    });

    return {
      FormControlElement: FormControlElement
    };
  }
};
