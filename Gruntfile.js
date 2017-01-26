module.exports = function(grunt){
  require('load-grunt-tasks')(grunt);
  var path = require('path');

  var statics = {
    web:   'web/static/web/',
    admin: 'web/static/admin/',
    build: 'web/static/build/'
  };
  
  // project global config
  var config = {
    project: 'rzero',
    pages: [{
      name: 'admin',
      root: statics.admin,
      css: {
        version: 1,
        lib: [
          'css/lib/spectrum.css'
        ],
        src: [
          'css/admin.scss'
        ]
      },
      js: {
        version: 2,
        devlib: [
          'js/lib/jquery.js',
          'js/lib/spectrum.js'
        ],
        lib: [
          'js/lib/jquery.min.js',
          'js/lib/spectrum.js'
        ],
        src: [
          'js/admin.js'
        ]
      }

    }, {
      name: 'chaos',
      root: statics.web,
      css: {
        version: 3,
        src: [
          'css/base.scss'
        ]
      },
      js: {
        version: 4,
        devlib: [
          'js/lib/jquery.js'
        ],
        lib: [
          'js/lib/jquery.min.js'
        ],
        src: [
          'js/base.js',
          'js/chaos.js'
        ]
      }

    }, {
      name: 'relief',
      root: statics.web,
      css: {
        version: 5,
        src: [
          'css/base.scss',
          'css/relief.scss'
        ]
      },
      js: {
        version: 6,
        devlib: [
          'js/lib/jquery.js'
        ],
        lib: [
          'js/lib/jquery.min.js'
        ],
        src: [
          'js/base.js',
          'js/chaos.js'
        ]
      }
    }]
  };

  // tasks
  var tasks = {
    compass: {},
    concat:  {},
    jshint:  {},
    uglify:  {},
    clean: {
      build: [
        path.join(statics.build)
      ],
      pages: [
        path.join(statics.admin, "*.js"),
        path.join(statics.admin, "*.css"),
        path.join(statics.web, "*.js"),
        path.join(statics.web, "*.css")
      ]
    }
  };

  for (var i = 0; i < config.pages.length; i++) {
    var p = config.pages[i];
    var mergeLibs = function(o) {
      if ('lib' in o) {
        if (!('devlib' in o)) {
          o['devlib'] = o.lib;
        }
      } else if ('devlib' in o) {
        o['lib'] = o.devlib;
      } else {
        o['lib'] = [];
        o['devlib'] = [];
      }
    };
    mergeLibs(p.css);
    mergeLibs(p.js);

    // COMPASS
    p.css.build = {
      dev: path.join(statics.build, p.name, "css-dev"),
      dist: path.join(statics.build, p.name, "css-dist")
    };
    tasks.compass[p.name + "-dev"] = {
      options: {
        specify: path.join(p.root, p.css.src),
        cssDir: p.css.build.dev,
        environment: 'development',
        outputStyle: 'nested',
        assetCacheBuster: false,
        raw: "sass_options = {:cache => false}\n"
      }
    };
    tasks.compass[p.name + "-dist"] = {
      options: {
        specify: path.join(p.root, p.css.src),
        cssDir: p.css.build.dist,
        environment: 'production',
        outputStyle: 'compressed',
        assetCacheBuster: false,
        raw: "sass_options = {:cache => false}\n"
      }
    };

    // CONCAT
    p.css.targets = {
      dev: path.join(p.root, p.name + "." + p.version + ".dev.css"),
      min: path.join(p.root, p.name + "." + p.version + ".min.css")
    };
    p.js.targets = {
      dev: path.join(p.name + "." + p.version + ".dev.js"),
      min: path.join(p.name + "." + p.version + ".min.js")
    };
    tasks.concat[p.name + "-dev-css"] = {
      src: p.css.devlib.concat(p.css.build.dev),
      dest: p.css.target.dev,
      options: { separator: '\n\n/*-- grunt-concat --*/\n\n' }
    };
    tasks.concat[p.name + "-dist-css"] = {
      src: p.css.lib.concat(p.css.build.dist),
      dest: p.css.target.dist,
      options: { separator: ';\n' }
    };
    tasks.concat[p.name + "-dev-js"] = {
      src: p.js.devlib.concat(p.js.src),
      dest: p.js.targets.dev,
      options: { separator: '\n\n/*-- grunt-concat --*/\n\n' }
    };
    tasks.concat[p.name + "-dist-js"] = {
      src: p.js.lib.concat(p.js.src),
      dest: p.js.targets.dist,
      options: { separator: ';\n' }
    };

    // JSHINT
    tasks.jshint[p.name] = p.js.src;

    // UGLIFY
    tasks.uglify[p.js.targets.dist] = p.js.targets.dist
  }

  grunt.registerTask('dist',    [
    'jshint',
    'compass:dist',  'concat:cssdist',
    'compass:admin', 'concat:cssadmin',
    'concat:jsdist', 'concat:jsadmin',
    'uglify',
    'clean:build'
  ]);

  grunt.registerTask('dev',     [
    'jshint',
    'compass:dev', 'compass:admin',
    'concat:cssdev',  'concat:cssadmin',
    'concat:jsdev',   'concat:jsadmin',
    'clean:build'
  ]);

  grunt.registerTask('all',     ['dev', 'dist']);
  grunt.registerTask('default', 'all');
};
