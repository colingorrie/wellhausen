<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <style>
            .text {
                margin: 0 5em 2em 5em;
            }
            .section {
                margin-bottom: 1em;
            }
            .one {
                background-color: #b3e2cd;
            }
            .two {
                background-color: #fdcdac;
            }
            .three {
                background-color: #cbd5e8;
            }
            .four {
                background-color: #f4cae4;
            }
            .five {
                background-color: #e6f5c9;
            }
        </style>
    </head>
    <body>
        % for i, text in enumerate(corpus.texts):
            <div class="text">
            <h2>${text.title}</h2>
            % for j, section in enumerate(text.sections):
                <div class="section ${cluster_names[cluster_assignments[i][j]]}">
                    ${str(section)}
                </div>
            % endfor
            </div>
        % endfor
        <p>Cluster assignments: ${cluster_assignments}</p>
    </body>
</html>