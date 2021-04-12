class CreateQueries:
    CREATE_TERMS = """
            DROP TABLE IF EXISTS terms CASCADE;
            CREATE TABLE terms (
                id                 varchar PRIMARY KEY,
                iri                varchar,
                label              varchar,
                description        varchar,
                ontology_name      varchar,
                ontology_prefix    varchar,
                ontology_iri       varchar,
                is_obsolete        BOOLEAN NOT NULL,
                term_replaced_by   varchar,
                is_defining_ontology BOOLEAN NOT NULL,
                has_children       BOOLEAN NOT NULL,
                is_root            BOOLEAN NOT NULL,
                obo_id             varchar,
                in_subset          varchar,
                is_preferred_root  BOOLEAN NOT NULL,
                parents            varchar
            );
        """

    CREATE_ONTOLOGY = """
            DROP TABLE IF EXISTS ontology CASCADE;
            CREATE TABLE ontology (
                id        varchar    PRIMARY KEY,
                iri                varchar,
                label              varchar,
                description        varchar,
                ontology_name      varchar,
                ontology_prefix    varchar,
                ontology_iri       varchar,
                is_obsolete        BOOLEAN NOT NULL,
                term_replaced_by   varchar,
                is_defining_ontology BOOLEAN NOT NULL,
                has_children       BOOLEAN NOT NULL,
                is_root            BOOLEAN NOT NULL,
                obo_id             varchar,
                in_subset          varchar,
                is_preferred_root  BOOLEAN NOT NULL
            );
        """

    CREATE_SYNONYMS = """
            DROP TABLE IF EXISTS Synonyms CASCADE;
            CREATE  TABLE Synonyms (
                id         serial PRIMARY KEY,
                synonyms          varchar
            );
        """

    CREATE_XREF = """
                DROP TABLE IF EXISTS Xref;
                CREATE  TABLE Xref (
                    id       serial PRIMARY KEY,
                    xref_id         varchar,
                    terms_id        varchar,
                    database        varchar,
                    description     varchar,
                    url             varchar,
                    CONSTRAINT fk_xref_terms_id FOREIGN KEY(terms_id) REFERENCES terms (id)
                );
            """
    CREATE_TERMS_SYNONYMS = """
                 DROP TABLE IF EXISTS terms_synonyms;
                 CREATE TABLE terms_synonyms (
                      terms_id varchar REFERENCES terms (id) ON UPDATE CASCADE ON DELETE CASCADE,
                      synonyms_id int REFERENCES synonyms (id) ON UPDATE CASCADE,
                      CONSTRAINT terms_synonyms_pkey PRIMARY KEY (terms_id, synonyms_id)  
                    );
            """

    CREATE_TERMS_ONTOLOGY = """
                     DROP TABLE IF EXISTS terms_ontology;
                     CREATE TABLE terms_ontology (
                          terms_id varchar REFERENCES terms (id) ON UPDATE CASCADE ON DELETE CASCADE,
                          ontology_id varchar REFERENCES ontology (id) ON UPDATE CASCADE
                        );
                """


class InsertQueries:
    INSERT_TERMS = """
                    INSERT INTO terms (id, iri, label, ontology_name,
                    ontology_prefix,ontology_iri,is_obsolete,term_replaced_by,
                    is_defining_ontology,has_children,is_root,obo_id,
                    in_subset, is_preferred_root, parents, description)
                    VALUES (
                        %(short_form)s,
                        %(iri)s,
                        %(label)s,
                        %(ontology_name)s,
                        %(ontology_prefix)s,
                        %(ontology_iri)s,
                        %(is_obsolete)s,
                        %(term_replaced_by)s,
                        %(is_defining_ontology)s,
                        %(has_children)s,
                        %(is_root)s,
                        %(obo_id)s,
                        %(in_subset)s,
                        %(is_preferred_root)s,
                        %(parents)s,
                        %(description)s
                    ) ON CONFLICT (id) DO NOTHING;
                """
    INSERT_ONTOLOGY = """
                    INSERT INTO Ontology (id, iri, label, ontology_name,
                    ontology_prefix,ontology_iri,is_obsolete,term_replaced_by,
                    is_defining_ontology,has_children,is_root,obo_id,
                    in_subset, is_preferred_root, description)
                    VALUES (
                        %(short_form)s,
                        %(iri)s,
                        %(label)s,
                        %(ontology_name)s,
                        %(ontology_prefix)s,
                        %(ontology_iri)s,
                        %(is_obsolete)s,
                        %(term_replaced_by)s,
                        %(is_defining_ontology)s,
                        %(has_children)s,
                        %(is_root)s,
                        %(obo_id)s,
                        %(in_subset)s,
                        %(is_preferred_root)s,
                        %(description)s
                        ) ON CONFLICT (id) DO NOTHING;
                """
    INSERT_SYNONYMS = """
                    INSERT INTO Synonyms (synonyms)
                    VALUES (
                        %(synonyms)s
                    );
                """

    INSERT_XREF = """
                        INSERT INTO Xref (database, xref_id, description, url, terms_id)
                        VALUES (
                            %(database)s,
                            %(id)s,
                            %(description)s,
                            %(url)s,
                            %(terms_id)s
                        );
                    """

    INSERT_TERMS_SYNONYMS = """
                        INSERT INTO terms_synonyms (terms_id, synonyms_id)
                        SELECT  %(terms_id)s, Synonyms.id
                        FROM Synonyms
                        WHERE Synonyms.synonyms = %(synonyms)s;
                    """

    INSERT_TERMS_ONTOLOGY = """
                            INSERT INTO terms_ontology (terms_id, ontology_id)
                            SELECT  %(child_terms_id)s, ontology.id
                            FROM ontology
                            WHERE ontology.id = %(parent_name)s;
                        """