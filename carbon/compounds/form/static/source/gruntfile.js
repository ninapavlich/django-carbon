module.exports = function(grunt) {

    //configure tasks
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        concat_css: {
            options: {
              // Task-specific options go here. 
            },
            forms: {
              src: ["css/*.css","css/vendor/*.css"],
              dest: "compiled/concat/carbon_forms.css"
            },
        },
        cssmin: {
            minify: {
                expand: true,
                cwd: 'compiled/concat/',
                src: ['*.css', '!*.min.css'],
                dest: 'compiled/min/',
                ext: '.min.css'
            }
        },      
        concat: {
            options: {
                separator: ';',
            },
            forms: {
                src: [
                    "js/vendor/*",
                    
                    "js/carbon_forms.js"
                ],
                dest: "compiled/concat/carbon_forms.js"
            }
        },

        uglify: {
            build: {
                files: {
                    'compiled/min/carbon_forms.min.js': ['compiled/concat/carbon_forms.js'],
                }
            }
        },
        copy: {
            scripts: {
                files:[{
                    expand: true,
                    cwd: 'compiled/concat/',
                    src: ['**/*.js'],
                    dest: '../js/'
                },{
                    expand: true,
                    cwd: 'compiled/min/',
                    src: ['**/*.js'],
                    dest: '../js/'
                }]
            },
            styles: {
                files: [{
                    expand: true,
                    cwd: 'compiled/concat/',
                    src: ['**/*.css'],
                    dest: '../css/'

                },{
                    expand: true,
                    cwd: 'compiled/min/',
                    src: ['**/*.css'],
                    dest: '../css/'

                }]
            }
        },  


        watch: {
            scripts: {
                files: ['js/*.js', 'js/*/*.js'],
                tasks: ['concat', 'uglify', 'copy:scripts'],
                options: {
                    spawn: false
                },
            }, 
            
            css: {
                files: ['css/*.css', 'css/*/*.css'],
                tasks: ['concat_css', 'cssmin:minify', 'copy:styles'],
                options: {
                    spawn: false
                }
            }
        }


    });


    
    // load plugins
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-compass');
    grunt.loadNpmTasks('grunt-newer');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-compress');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-concat-css');
    
    // register tasks
    grunt.registerTask(
        'default',
        [
            'concat',
            'uglify',
            'copy:scripts',
            'concat_css',
            'cssmin:minify',
            'copy:styles',
            'watch'
        ]
    );
};