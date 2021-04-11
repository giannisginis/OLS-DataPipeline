class DatabaseMetadata:
    POSTGRES_USER = 'root'
    POSTGRES_PASSWORD = 'root'
    POSTGRES_HOST = 'localhost'
    POSTGRES_PORT = 5432
    db_name = 'DataPipeline'


class OntologyLookupService:
    API = 'http://www.ebi.ac.uk/ols/api/ontologies/'


class CreateQueries:
    CREATE_TERMS = """
            DROP TABLE IF EXISTS terms;
            CREATE TABLE terms (
                id        serial    PRIMARY KEY,
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
                short_form         varchar,
                obo_id             varchar,
                in_subset          varchar,
                is_preferred_root  BOOLEAN NOT NULL,
                parents            varchar
            );
        """

    CREATE_ONTOLOGY = """
            DROP TABLE IF EXISTS Ontology;
            CREATE TABLE Ontology (
                id        serial    PRIMARY KEY,
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
                short_form         varchar,
                obo_id             varchar,
                in_subset          varchar,
                is_preferred_root  BOOLEAN NOT NULL,
                child_id              varchar
            );
        """

    CREATE_SYNONYMS = """
            DROP TABLE IF EXISTS Synonyms;
            CREATE  TABLE Synonyms (
                id         serial PRIMARY KEY,
                terms_id          varchar,
                synonyms          varchar
            );
        """


class InsertQueries:
    INSERT_TERMS = """
                    INSERT INTO terms (iri, label, ontology_name,
                    ontology_prefix,ontology_iri,is_obsolete,term_replaced_by,
                    is_defining_ontology,has_children,is_root,short_form,obo_id,
                    in_subset, is_preferred_root, parents, description)
                    VALUES (
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
                        %(short_form)s,
                        %(obo_id)s,
                        %(in_subset)s,
                        %(is_preferred_root)s,
                        %(parents)s,
                        %(description)s
                    );
                """
    INSERT_ONTOLOGY = """
                    INSERT INTO Ontology (iri, label, ontology_name,
                    ontology_prefix,ontology_iri,is_obsolete,term_replaced_by,
                    is_defining_ontology,has_children,is_root,short_form,obo_id,
                    in_subset, is_preferred_root, description, child_id)
                    VALUES (
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
                        %(short_form)s,
                        %(obo_id)s,
                        %(in_subset)s,
                        %(is_preferred_root)s,
                        %(description)s,
                        %(child_id)s
                    );
                """
    INSERT_SYNONYMS = """
                    INSERT INTO Synonyms (synonyms, terms_id)
                    VALUES (
                        %(synonyms)s,
                        %(terms_id)s
                    );
                """


class UpdateQueries:
    pass