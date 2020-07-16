module.exports = function(grunt) {

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        copy: {
            main: {
                files: [
                    { expand: true, cwd: 'node_modules/uikit/dist/css/', src: 'uikit.css', dest: 'assets/', filter: 'isFile' },
                    { expand: true, cwd: 'node_modules/uikit/dist/js/', src: 'uikit.js', dest: 'assets/', filter: 'isFile' },
                    { expand: true, cwd: 'node_modules/uikit/dist/js/', src: 'uikit-icons.js', dest: 'assets/', filter: 'isFile' },
                    { expand: true, cwd: 'node_modules/uikit/src/scss/', src: '*', dest: 'resources/sass/uikit/', filter: 'isFile' },
                    { expand: true, cwd: 'node_modules/uikit/src/js/', src: '*', dest: 'resources/js/uikit/', filter: 'isFile' },
                ],
            },
        }
    });

    grunt.loadNpmTasks('grunt-contrib-copy');

    grunt.registerTask('default', ['copy']);

};