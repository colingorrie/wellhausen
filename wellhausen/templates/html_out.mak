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
        </style>
    </head>
    <body>
        % for text in corpus.texts:
            <div class="text">
            % for section in text.sections:
                <div class="section">
                    ${str(section)}
                </div>
            % endfor
            </div>
        % endfor
        <p>Cluster assignments: ${cluster_assignments}</p>
    </body>
</html>